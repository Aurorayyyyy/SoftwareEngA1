from typing import List, Tuple

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import yaml

from utils import extract_product_id_and_quantity

app = Flask(__name__)
cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
host = cred['mysql_host']
user = cred['mysql_user']
password = cred['mysql_password']
db_name = cred['mysql_db']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}/{db_name}'

db = SQLAlchemy(app)

from models import VendingMachine, Product, VendingMCProduct


@app.route('/')
def index():  # put application's code here
    return 'Welcome to Vending Machine Tracking Application.' \
           'Try to read readme.md in the github repo if you do not ' \
           'understand '


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

    prod_id_and_quantity_list = extract_product_id_and_quantity(data['pid'])
    for prod_id_and_quantity in prod_id_and_quantity_list:
        product_id, quantity = prod_id_and_quantity
        add_product_to_machine(machine.id, product_id, quantity)
    return jsonify(machine)


@app.route('/machines/edit/<int:mc_id>', methods=['POST'])
def edit_machine(machine_id: int):
    data = request.form
    machine = VendingMachine.find_by_id(machine_id)
    if machine:
        machine.name = data['name']
        machine.location = data['location']
        db.session.commit()

        list_prod_id_and_quantity = extract_product_id_and_quantity(data['pid'])
        all_product_id_in_machine = get_formatting_list_of_product_id(machine.id, list_prod_id_and_quantity)

        for relation in VendingMCProduct.get_all_relation_by_mc(machine.id):
            if relation.product_id not in all_product_id_in_machine:
                VendingMCProduct.delete(machine.id, relation.product_id)
        return jsonify(machine)
    return jsonify(Error="Machine not found")


def get_formatting_list_of_product_id(machine_id: int, raw_list: List[Tuple[int, int]]) -> List[int]:
    return_list: List[int] = []
    for elem in raw_list:
        product_id, product_quantity = elem
        relation = VendingMCProduct.get(machine_id, product_id)
        if relation:
            edit_product_in_machine(machine_id, product_id, product_quantity)
            return_list.append(product_id)
        else:
            add_product_to_machine(machine_id, product_id, product_quantity)
            return_list.append(product_id)
    return return_list


@app.route('/machines/delete/<int:mc_id>', methods=['POST'])
def delete_machine(machine_id):
    machine = VendingMachine.find_by_id(machine_id)
    if machine:
        relations = VendingMCProduct.get_all_relation_by_mc(machine_id)
        if relations:
            for relation in relations:
                VendingMCProduct.delete(machine.id, relation.product_id)
            db.session.commit()
        VendingMachine.delete(machine.id)
        return jsonify(Message="Delete Successful")
    return jsonify(Error="Machine not found")


def edit_product_in_machine(machine_id: int, product_id: int, quantity: int):
    machine = VendingMachine.find_by_id(machine_id)
    if machine:
        relation = VendingMCProduct.get(machine.id, product_id)
        relation.quantity = quantity
        db.session.commit()
        return jsonify(machine)
    return jsonify(Error="Machine not found")


def delete_product_in_machine(machine_id: int, product_id: int):
    machine = VendingMachine.find_by_id(machine_id)
    if machine:
        relation = VendingMCProduct.get(machine.id, product_id)
        if relation:
            VendingMCProduct.delete(machine.id, product_id)
            return jsonify(Message="Delete successful")
    return jsonify(Error="Machine not found or There is no product in this machine")


def add_product_to_machine(machine_id: int, product_id: int, quantity: int):
    machine = VendingMachine.find_by_id(machine_id)
    if machine:
        new_product = machine.add_product(product_id, quantity)
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


@app.route('/products/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id: int):
    data = request.form
    product = Product.find_by_id(product_id)
    if product:
        product.name = data['name']
        product.price = data['price']
        db.session.commit()
        return jsonify(product)
    return jsonify(Error='Product not found')


@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id: int):
    product: Product = Product.find_by_id(product_id)
    if product:
        relations: List[VendingMCProduct] = VendingMCProduct.get_all_relation_by_prod(product_id)
        if relations:
            for relation in relations:
                VendingMCProduct.delete(relation.vendingMC_id, product_id)
            db.session.commit()
        Product.delete(product.id)
        return jsonify(Message="Delete Successful")
    return jsonify(Error="Product not found")


if __name__ == '__main__':
    app.run()
