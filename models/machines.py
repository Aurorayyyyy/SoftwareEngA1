from dataclasses import dataclass
from typing import List, Tuple

from extensions import db
from models.products import Product
from models.stocks import VendingMCProduct


@dataclass
class VendingMachine(db.Model):
    id: int
    name: str
    location: str
    machine_products: List["VendingMCProduct"]

    id = db.Column("vendingMC_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(30), nullable=False, unique=True)
    location = db.Column("location", db.String(255), nullable=False)
    products = db.relationship("VendingMCProduct", backref="machine", lazy=True)

    @property
    def machine_products(self) -> List[dict]:
        stocks = VendingMCProduct.query.filter_by(vendingMC_id=self.id).all()
        return [stock.to_dict() for stock in stocks]

    def edit_machine_name_and_location(self, name: str, location: str):
        if name != "None":
            self.name = name
        if location != "None":
            self.location = location
        db.session.commit()

    def add_product(self, product_id: int, quantity: int):
        if Product.find_by_id(product_id):
            stock = VendingMCProduct(
                vendingMC_id=self.id, product_id=product_id, quantity=quantity
            )
            db.session.add(stock)
            db.session.commit()

    def add_product_to_the_stock(self, product_id: int, quantity: int):
        machine = VendingMachine.find_by_id(self.id)
        if machine:
            machine.add_product(product_id, quantity)

    def edit_product_in_machine(self, product_id: int, quantity: int):
        machine = VendingMachine.find_by_id(self.id)
        if machine:
            relation = VendingMCProduct.get(machine.id, product_id)
            relation.quantity = quantity
            db.session.commit()

    def get_formatting_list_of_product_id_after_edit(
        self, raw_list: List[Tuple[int, int]]
    ) -> List[int]:
        return_list: List[int] = []
        for elem in raw_list:
            product_id, product_quantity = elem
            relation = VendingMCProduct.get(self.id, product_id)
            if relation:
                self.edit_product_in_machine(product_id, product_quantity)
                return_list.append(product_id)
            else:
                self.add_product_to_the_stock(product_id, product_quantity)
                return_list.append(product_id)
        return return_list

    @staticmethod
    def delete_all_relation_in_machine(machine_id: int):
        machine = VendingMachine.find_by_id(machine_id)
        if machine:
            relations = VendingMCProduct.get_all_relation_by_mc(machine_id)
            if relations:
                for relation in relations:
                    VendingMCProduct.delete(machine.id, relation.product_id)
                db.session.commit()

    @staticmethod
    def add_machine(name: str, location: str):
        machine = VendingMachine.find_by_name(name)
        if machine is None:
            new_machine = VendingMachine(name=name, location=location)
            db.session.add(new_machine)
            db.session.commit()

    @staticmethod
    def find_by_id(machine_id: int) -> "VendingMachine":
        return VendingMachine.query.get(machine_id)

    @staticmethod
    def find_by_name(name: str) -> "VendingMachine":
        return VendingMachine.query.filter_by(name=name).first()

    @staticmethod
    def delete(machine_id: int):
        VendingMachine.query.filter_by(id=machine_id).delete()
        db.session.commit()

    @staticmethod
    def get_all() -> "VendingMachine":
        return VendingMachine.query.all()
