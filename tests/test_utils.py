from flask import Flask


# from models.products import Product
# from models.stocks import VendingMCProduct
from utils import extract_product_id_and_quantity

# have to change open('cred.yaml') to open('../cred.yaml') to run the unittest.


def test_extract_product_id_and_quantity(app: Flask):

    #     # add_product_to_machine(1,2,3)
    #     machine1 = VendingMachine(name="testUnittest", location="location")
    #     prod1 = Product(name="prodTestUnitest", price="98")
    #
    #     quantity1 = 100
    #     machine1.add_product_to_the_stock(product_id=prod1.id, quantity=quantity1)
    #     relation1 = VendingMCProduct.get(machine1.id, prod1.id)
    #     print(relation1.quantity)
    #     assert relation1.quantity == quantity1

    test1 = extract_product_id_and_quantity("(1:2),(2:3),(4:5)")
    test2 = extract_product_id_and_quantity("(1:2)")
    test3 = extract_product_id_and_quantity("(1:2),(4:6)")
    test4 = extract_product_id_and_quantity("(2:2),(3:8)")
    assert test1 == [(1, 2), (2, 3), (4, 5)]
    assert test2 == [(1, 2)]
    assert test3 == [(1, 2), (4, 6)]
    assert test4 == [(2, 2), (3, 8)]
