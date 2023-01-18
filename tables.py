
from app import db, app
from dataclasses import dataclass
from typing import List



@dataclass
class VendingMachine(db.Model):

    id: int
    name: str
    location: str
    products: List["VendingMCProduct"]

    id = db.Column('vendingMC_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(30), nullable=False, unique=True)
    location = db.Column('location', db.String(255), nullable=False)
    products = db.relationship('VendingMCProduct', backref='machine', lazy=True)

    def get_all(self):
        return VendingMachine.query.all()
    # def find(self, pd_id):
    #     return VendingMCProduct.get(self.id, pd_id)
    def add_product(self, product_id, quantity):
        if Product.find_by_id(product_id):
            return VendingMCProduct(vendingMC_id=self.id, product_id=product_id, quantity=quantity)
        return None

    @staticmethod
    def find_by_id(id):
        return VendingMachine.query.get(id)

    @staticmethod
    def delete(vm_id):
        VendingMachine.query.filter_by(id=vm_id).delete()
        db.session.commit()




@dataclass
class Product(db.Model):
    id: int
    name: str
    price: int

    id = db.Column('product_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(30), nullable=False, unique=True)
    price = db.Column('price', db.Integer)
    belong = db.relationship('VendingMCProduct', backref='product', lazy=True)

    @staticmethod
    def find_by_id(p_id):
        return Product.query.get(p_id)


@dataclass
class VendingMCProduct(db.Model):
    product_id: int
    quantity: int

    vendingMC_id = db.Column(db.Integer, db.ForeignKey('vending_machine.vendingMC_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get(vm_id, p_id):
        return VendingMCProduct.query.filter_by(vendingMC_id=vm_id, product_id=p_id).first()

    @staticmethod
    def get_all_product(vm_id):
        return VendingMCProduct.query.filter_by(vendingMC_id=vm_id).all()

    @staticmethod
    def delete(vm_id, p_id):
        VendingMCProduct.query.filter_by(vendingMC_id=vm_id, product_id=p_id).delete()
        db.session.commit()



        # same_product_id = VendingMCProduct.vendingMC_id == vm_id
        # same_machine_id = VendingMCProduct.product_id == mc_id
        # VendingMCProduct.query.filter_by(
        #     (same_product_id) and
        #     (same_machine_id)
        # ).first()

if __name__ == '__main__':
    # test database
    with app.app_context():
        db.drop_all()
        db.create_all()

        mc1 = VendingMachine(name='vendingMc1', location='location')
        mc2 = VendingMachine(name='vendingMc2', location='location')
        mc3 = VendingMachine(name='vendingMc3', location='location')
        mc4 = VendingMachine(name='vendingMc4', location='location')
        pd1 = Product(name='product1', price='100')
        pd2 = Product(name='product2', price='10')
        pd3 = Product(name='product3', price='20')
        pd4 = Product(name='product4', price='50')
        pd5 = Product(name='product5', price='30')

        re1 = VendingMCProduct(vendingMC_id='1', product_id='1', quantity='10')
        re2 = VendingMCProduct(vendingMC_id='2', product_id='2', quantity='20')
        re3 = VendingMCProduct(vendingMC_id='3', product_id='3', quantity='30')
        re4 = VendingMCProduct(vendingMC_id='4', product_id='4', quantity='40')
        re5 = VendingMCProduct(vendingMC_id='1', product_id='5', quantity='5')
        db.session.add(mc1)
        db.session.add(mc2)
        db.session.add(mc3)
        db.session.add(mc4)

        db.session.add(pd1)
        db.session.add(pd2)
        db.session.add(pd3)
        db.session.add(pd4)
        db.session.add(pd5)

        db.session.add(re1)
        db.session.add(re2)
        db.session.add(re3)
        db.session.add(re4)
        db.session.add(re5)

        db.session.commit()
