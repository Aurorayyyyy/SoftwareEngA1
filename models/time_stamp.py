from dataclasses import dataclass
from datetime import datetime
from typing import List

from flask import jsonify
from sqlalchemy import JSON

from extensions import db
from models.stocks import VendingMCProduct
import datetime as dt


@dataclass
class TimeStamp(db.Model):
    vending_machine_id: int
    product_id: int
    quantity: int
    state: JSON
    date: datetime

    id = db.Column("time_stamp_id", db.Integer, primary_key=True, autoincrement=True)
    vending_machine_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    state = db.Column(db.JSON, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def add_time_stamp(vending_machine_id: int, product_id: int, quantity: int):

        db.session.add(
            TimeStamp(
                vending_machine_id=vending_machine_id,
                product_id=product_id,
                quantity=quantity,
                state=jsonify(
                    VendingMCProduct.get_all_relation_by_mc(vending_machine_id)
                ).json,
                date=dt.datetime.utcnow(),
            )
        )
        db.session.commit()

    @staticmethod
    def get_all_stocks(machine_id: int) -> "TimeStamp":
        return TimeStamp.query.filter_by(vending_machine_id=machine_id).all()

    @staticmethod
    def get_all_products(product_id: int) -> List[dict]:
        time_stamps = TimeStamp.query.filter_by(product_id=product_id).all()
        products = []
        for time_stamp in time_stamps:
            products.append(
                {
                    "product_id": time_stamp.product_id,
                    "quantity": time_stamp.quantity,
                    "date": time_stamp.date,
                }
            )
        return products
