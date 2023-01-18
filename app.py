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

from tables import VendingMachine, Product


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
    machine = VendingMachine(name=data['name'], location=data['location'])
    db.session.add(machine)
    db.session.commit()

    list_tuple_data = extract_pid_quantity(data['pid'])
    for elem in list_tuple_data:
        p_id, p_qt = elem
        # do not care about the return
        _ = add_product_to_machine(machine.id, p_id, p_qt)
    return jsonify(machine)



@app.route('/machines/edit/<int:m_id>', methods=['POST'])
def edit_machine(m_id):
    data = request.form

    machine = VendingMachine.find_by_id(m_id)
    machine.name = data['name']
    machine.location = data['location']

    db.session.commit()
    return jsonify(machine)


# @app.route('/machines/<int:mc_id>/add_product/<int:p_id>', methods=['POST'])
def add_product_to_machine(mc_id, p_id, quantity):
    machine = VendingMachine.find_by_id(mc_id)
    if machine:
        new_product = machine.add_product(p_id, quantity)
        print(new_product)
        db.session.add(new_product)
        db.session.commit()
        return jsonify(machine)
    return jsonify(Error="Machine not found")


# @app.route('/machines/<int:mc_id>/edit/<>/', methods=['POST'])
# def edit_machine()


if __name__ == '__main__':
    # from tables import VendingMachine

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #
    #     mc = VendingMachine()
    #     db.session.add(mc)

    app.run()
