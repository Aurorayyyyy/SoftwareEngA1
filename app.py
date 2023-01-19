from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import yaml

from utils import extract_pid_quantity

app = Flask(__name__)
cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
host = cred['mysql_host']
user = cred['mysql_user']
password = cred['mysql_password']
db_name = cred['mysql_db']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}/{db_name}'

db = SQLAlchemy(app)

from tables import VendingMachine, Product, VendingMCProduct


@app.route('/')
def index():  # put application's code here
    return 'Hello World!'


@app.route('/machines', methods=['GET'])
def get_all_machines():
    return jsonify(VendingMachine.query.all())


@app.route('/products', methods=['GET'])
def get_all_product():
    return jsonify(Product.query.all())


@app.route('/machines/add', methods=['POST'])
def add_machine():
    data = request.form
    VendingMachine.add_machine(data['name'], data['location'])
    machine = VendingMachine.find_by_name(name=data['name'])

    list_tuple_data = extract_pid_quantity(data['pid'])
    for elem in list_tuple_data:
        p_id, p_qt = elem
        # do not care about the return
        _ = add_product_to_machine(machine.id, p_id, p_qt)
    return jsonify(machine)


@app.route('/machines/edit/<int:mc_id>', methods=['POST'])
def edit_machine(mc_id):
    data = request.form
    machine = VendingMachine.find_by_id(mc_id)
    if machine:
        machine.name = data['name']
        machine.location = data['location']
        db.session.commit()

        list_tuple_data = extract_pid_quantity(data['pid'])
        # list of p_id that should be
        list_new_data = []
        num_new_products = 0
        for elem in list_tuple_data:
            p_id, p_qt = elem
            relation = VendingMCProduct.get(machine.id, p_id)
            if relation:
                edit_product_in_machine(machine.id, p_id, p_qt)
                num_new_products += 1
                list_new_data.append(p_id)
            else:
                add_product_to_machine(machine.id, p_id, p_qt)
                num_new_products += 1
                list_new_data.append(p_id)

        # if len(list_new_data) != num_new_products:
        for rel in VendingMCProduct.get_all_relation_by_mc(machine.id):
            if rel.product_id not in list_new_data:
                VendingMCProduct.delete(machine.id, rel.product_id)
        return jsonify(machine)
    return jsonify(Error="Machine not found")


@app.route('/machines/delete/<int:mc_id>', methods=['POST'])
def delete_machine(mc_id):
    machine = VendingMachine.find_by_id(mc_id)
    if machine:
        relation = VendingMCProduct.get_all_relation_by_mc(mc_id)
        if relation:
            for each in relation:
                VendingMCProduct.delete(machine.id, each.product_id)
            db.session.commit()
        VendingMachine.delete(machine.id)
        return jsonify(Message="Delete Successful")
    return jsonify(Error="Machine not found")

def edit_product_in_machine(mc_id, p_id, quantity):
    machine = VendingMachine.find_by_id(mc_id)
    if machine:
        relation = VendingMCProduct.get(machine.id, p_id)
        # print(relation)
        relation.quantity = quantity
        db.session.commit()
        return jsonify(machine)
    return jsonify(Error="Machine not found")


def delete_product_in_machine(mc_id, p_id):
    machine = VendingMachine.find_by_id(mc_id)
    if machine:
        relation = VendingMCProduct.get(machine.id, p_id)
        if relation:
            VendingMCProduct.delete(machine.id, p_id)
            return jsonify(Message="Delete successful")
    return jsonify(Error="Machine not found or There is no product in this machine")


def add_product_to_machine(mc_id, p_id, quantity):
    machine = VendingMachine.find_by_id(mc_id)
    if machine:
        new_product = machine.add_product(p_id, quantity)
        print(new_product)
        db.session.add(new_product)
        db.session.commit()
        return jsonify(machine)
    return jsonify(Error="Machine not found")

@app.route('/products/add', methods=['POST'])
def add_product():
    data = request.form
    Product.add_product(data['name'], data['price'])
    product = Product.find_by_name(name=data['name'])
    return jsonify(product)

@app.route('/products/edit/<int:p_id>', methods=['POST'])
def edit_product(p_id):
    data = request.form
    product = Product.find_by_id(p_id)
    if product:
        product.name = data['name']
        product.price = data['price']
        db.session.commit()
        return jsonify(product)
    return jsonify(Error='Product not found')

@app.route('/products/delete/<int:p_id>', methods=['POST'])
def delete_product(p_id):
    product = Product.find_by_id(p_id)
    if product:
        relation = VendingMCProduct.get_all_relation_by_prod(p_id)
        if relation:
            for each in relation:
                VendingMCProduct.delete(each.vendingMC_id, p_id)
            db.session.commit()
        Product.delete(product.id)
        return jsonify(Message="Delete Successful")
    return jsonify(Error="Product not found")





if __name__ == '__main__':
    # from tables import VendingMachine
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #
    #     mc = VendingMachine()
    #     db.session.add(mc)
    app.run()
