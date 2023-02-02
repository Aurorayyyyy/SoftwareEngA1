import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.conftest import Tester


class ProductTester(Tester):
    def get_all(self) -> TestResponse:
        return self.client.get("/products")

    def post_product_add(self, name: str, price: str) -> TestResponse:
        return self.client.post(
            "/products/add",
            data={
                "name": name,
                "price": price,
            },
        )

    def post_product_edit(self, product_id: int, name: str, price: str) -> TestResponse:
        return self.client.post(
            f"/products/edit/{product_id}",
            data={
                "name": name,
                "price": price,
            },
        )

    def post_product_edit_price_only(self, product_id: int, price: str) -> TestResponse:
        return self.client.post(
            f"/products/edit/{product_id}",
            data={
                "price": price,
            },
        )

    def post_product_edit_name_only(self, product_id: int, name: str) -> TestResponse:
        return self.client.post(
            f"/products/edit/{product_id}",
            data={
                "name": name,
            },
        )

    def post_product_edit_without_name_and_price(self, product_id: int) -> TestResponse:
        return self.client.post(f"/products/edit/{product_id}")

    def post_product_delete(self, product_id: int) -> TestResponse:
        return self.client.post(f"/products/delete/{product_id}")


@pytest.fixture()
def tester(client: FlaskClient) -> ProductTester:
    return ProductTester(client=client)


def test_get_all(tester: ProductTester):
    get_all_response = tester.get_all()
    assert get_all_response.json == []


def test_add_product(tester: ProductTester):
    add_product1 = tester.post_product_add("test_name1", "100")
    add_product2 = tester.post_product_add("test_name2", "102")
    add_product3 = tester.post_product_add("test_name3", "104")
    assert add_product1.json == {"id": 1, "name": "test_name1", "price": 100}
    assert add_product2.json == {"id": 2, "name": "test_name2", "price": 102}
    assert add_product3.json == {"id": 3, "name": "test_name3", "price": 104}


def test_edit_product(tester: ProductTester):
    tester.post_product_add("test_name", "100")
    add_product = tester.post_product_edit_price_only(1, "101")
    print(add_product.json)
    assert add_product.json == {"id": 1, "name": "test_name", "price": 101}
    add_product = tester.post_product_edit_name_only(1, "test_name1")
    assert add_product.json == {"id": 1, "name": "test_name1", "price": 101}
    add_product = tester.post_product_edit_without_name_and_price(1)
    assert add_product.json == {"id": 1, "name": "test_name1", "price": 101}
    add_product = tester.post_product_edit(1, "test_name", "100")
    assert add_product.json == {"id": 1, "name": "test_name", "price": 100}


def test_delete_product(tester: ProductTester):
    tester.post_product_add("test_name1", "100")
    tester.post_product_add("test_name2", "100")
    tester.post_product_add("test_name3", "100")
    tester.post_product_add("test_name4", "100")
    tester.post_product_add("test_name5", "100")

    delete1 = tester.post_product_delete(1)
    assert delete1.json == {"Message": "Delete Successful"}
    tester.post_product_delete(2)
    tester.post_product_delete(3)
    tester.post_product_delete(4)
    tester.post_product_delete(5)

    get_all_response = tester.get_all()
    assert get_all_response.json == []
