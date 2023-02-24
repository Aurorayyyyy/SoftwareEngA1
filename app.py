import yaml
from flask import Blueprint, Flask, Response, jsonify, request
from flask_wtf import CSRFProtect
from flask_swagger_ui import get_swaggerui_blueprint

from extensions import db
from models.machines import VendingMachine
from models.products import Product
from models.stocks import VendingMCProduct
from models.time_stamp import TimeStamp
from utils import reformatting_product_id_and_quantity

machine_not_found = "Machine not found"
product_not_found = "Product not found"
invalid_missing_input = "Invalid/missing input"


def create_app() -> Flask:
    app = Flask(__name__)
    csrf = CSRFProtect()
    csrf.init_app(app)
    cred = yaml.load(open("cred.yaml"), Loader=yaml.Loader)
    host = cred["mysql_host"]
    user = cred["mysql_user"]
    password = cred["mysql_password"]
    db_name = cred["mysql_db"]

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql://{user}:{password}@{host}/{db_name}"
    db.init_app(app)

    # register blueprints
    app.register_blueprint(bp)

    SWAGGER_URL = "/swagger"
    API_URL = "../static/openapi.yaml"
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "vending_machine"}
    )

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app


def reset_database(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()


bp = Blueprint("app", __name__)


@bp.route("/")
def index():  # noqa: ANN201
    return (
        "Welcome to Vending Machine Tracking Application."
        "Try to read readme.md in the github repo if you do not "
        "understand "
    )


@bp.route("/machines", methods=["GET"])
def get_all_machines() -> Response:
    return jsonify(VendingMachine.get_all())


@bp.route("/products", methods=["GET"])
def get_all_product() -> Response:
    return jsonify(Product.get_all())


@bp.route("/machines/add", methods=["POST"])
def add_machine() -> Response:
    data = request.form
    if data.get("name") is not None and data.get("location") is not None:
        VendingMachine.add_machine(data["name"], data["location"])
        machine = VendingMachine.find_by_name(name=data["name"])
        if data.get("pid") != "" and data.get("pid") is not None:
            prod_id_and_quantity_list = reformatting_product_id_and_quantity(
                data["pid"]
            )
            for prod_id_and_quantity in prod_id_and_quantity_list:
                product_id, quantity = prod_id_and_quantity
                machine.add_product_to_the_stock(product_id, quantity)
        return jsonify(machine)
    return jsonify(Error=invalid_missing_input)


@bp.route("/machines/edit/<int:machine_id>", methods=["POST"])
def edit_machine(machine_id: int) -> Response:
    data = request.form
    machine = VendingMachine.find_by_id(machine_id)
    if machine:
        if data.get("name") is not None and data.get("location") is not None:
            machine.edit_machine_name_and_location(
                str(data.get("name")), str(data.get("location"))
            )
        if data.get("name") is not None:
            machine.edit_machine_name(str(data.get("name")))
        elif data.get("location") is not None:
            machine.edit_machine_location(str(data.get("location")))

        all_product_id_in_machine = list(tuple())
        if data.get("pid") is not None and data.get("pid") != "":
            list_prod_id_and_quantity = reformatting_product_id_and_quantity(
                data["pid"]
            )
            all_product_id_in_machine = (
                machine.get_formatting_list_of_product_id_after_edit(
                    list_prod_id_and_quantity
                )
            )
        if data.get("pid") is not None:
            for relation in VendingMCProduct.get_all_relation_by_mc(machine.id):
                if relation.product_id not in all_product_id_in_machine:
                    VendingMCProduct.delete(machine.id, relation.product_id)
                    TimeStamp.add_time_stamp(
                        vending_machine_id=machine.id,
                        product_id=relation.product_id,
                        quantity=0,
                    )
        return jsonify(machine)
    return jsonify(Error=machine_not_found)


@bp.route("/machines/delete/<int:machine_id>", methods=["POST"])
def delete_machine(machine_id: int) -> Response:
    machine = VendingMachine.find_by_id(machine_id)
    if machine:
        VendingMachine.delete_all_relation_in_machine(machine_id)
        VendingMachine.delete(machine_id)
        return jsonify(Message="Delete Successful")
    return jsonify(Error=machine_not_found)


@bp.route("/products/add", methods=["POST"])
def add_product() -> Response:
    data = request.form
    if data.get("name") is not None and data.get("price") is not None:
        Product.add_product(data["name"], int(data["price"]))
        product = Product.find_by_name(name=data["name"])
        return jsonify(product)
    return jsonify(Error=invalid_missing_input)


@bp.route("/products/edit/<int:product_id>", methods=["POST"])
def edit_product(product_id: int) -> Response:
    data = request.form
    product = Product.find_by_id(product_id)
    if product:
        product.edit_product(str(data.get("name")), str(data.get("price")))
        return jsonify(product)
    return jsonify(Error=product_not_found)


@bp.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id: int) -> Response:
    product: Product = Product.find_by_id(product_id)
    if product:
        Product.delete_all_relation_in_product(product.id)
        Product.delete(product_id)
        return jsonify(Message="Delete Successful")
    return jsonify(Error=product_not_found)


@bp.route("/time_stamp/all_stocks/<int:machine_id>", methods=["GET"])
def get_all_stocks_time_stamps(machine_id: int) -> Response:
    machine: VendingMachine = VendingMachine.find_by_id(machine_id)
    if machine:
        return jsonify(TimeStamp.get_all_stocks(machine_id))
    return jsonify(Error=machine_not_found)


@bp.route("/time_stamp/all_products/<int:product_id>", methods=["GET"])
def get_all_products_time_stamps(product_id: int) -> Response:
    product: Product = Product.find_by_id(product_id)
    if product:
        return jsonify(TimeStamp.get_all_products(product_id))
    return jsonify(Error=product_not_found)


if __name__ == "__main__":
    app = create_app()
    app.run()
