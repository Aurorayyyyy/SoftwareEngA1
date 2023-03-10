from flask import Flask

from utils import (
    reformatting_product_id_and_quantity,
)


# have to change open('cred.yaml') to open('../cred.yaml') to run the unittest.


def test_extract_product_id_and_quantity(app: Flask):

    test1 = reformatting_product_id_and_quantity("(1:2),(2:3),(4:5)")
    test2 = reformatting_product_id_and_quantity("(1:2)")
    test3 = reformatting_product_id_and_quantity("(1:2),(4:6)")
    test4 = reformatting_product_id_and_quantity("(2:2),(3:8)")
    assert test1 == [(1, 2), (2, 3), (4, 5)]
    assert test2 == [(1, 2)]
    assert test3 == [(1, 2), (4, 6)]
    assert test4 == [(2, 2), (3, 8)]
