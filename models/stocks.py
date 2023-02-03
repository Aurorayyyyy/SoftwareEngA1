from dataclasses import dataclass
from typing import List

from extensions import db


@dataclass
class VendingMCProduct(db.Model):
    product_id: int
    quantity: int

    vendingMC_id = db.Column(
        db.Integer, db.ForeignKey("vending_machine.vendingMC_id"), primary_key=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.product_id"), primary_key=True
    )
    quantity = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get(machine_id: int, product_id: int) -> "VendingMCProduct":
        return VendingMCProduct.query.filter_by(
            vendingMC_id=machine_id, product_id=product_id
        ).first()

    @staticmethod
    def get_all_relation_by_mc(machine_id: int) -> "VendingMCProduct":
        return VendingMCProduct.query.filter_by(vendingMC_id=machine_id).all()

    @staticmethod
    def get_all_relation_by_prod(product_id: int) -> "VendingMCProduct":
        return VendingMCProduct.query.filter_by(product_id=product_id).all()

    @staticmethod
    def delete(machine_id: int, product_id: int):
        VendingMCProduct.query.filter_by(
            vendingMC_id=machine_id, product_id=product_id
        ).delete()
        db.session.commit()

    @staticmethod
    def delete_all_relation_in_product(product_id: int):
        relations: List[VendingMCProduct] = VendingMCProduct.get_all_relation_by_prod(
            product_id
        )
        if relations:
            for relation in relations:
                VendingMCProduct.delete(relation.vendingMC_id, product_id)
            db.session.commit()

    def to_dict(self) -> dict:
        return {"product_id": self.product_id, "quantity": self.quantity}
