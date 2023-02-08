import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.conftest import Tester
from tests.test_machine_route import MachineTester
from tests.test_product_route import ProductTester


class TimeStampTester(Tester):
    def get_all_stocks_time_stamps(self, machine_id: int) -> TestResponse:
        return self.client.get(f"/time_stamp/all_stocks/{machine_id}")

    def get_all_products_time_stamps(self, product_id: int) -> TestResponse:
        return self.client.get(f"/time_stamp/all_products/{product_id}")


@pytest.fixture
def tester_time_stamp(client: FlaskClient) -> TimeStampTester:
    return TimeStampTester(client)


@pytest.fixture()
def tester_machine(client: FlaskClient) -> MachineTester:
    return MachineTester(client=client)


@pytest.fixture()
def tester_product(client: FlaskClient) -> ProductTester:
    return ProductTester(client=client)


def test_get_stocks_time_stamps(
    tester_time_stamp: TimeStampTester,
    tester_machine: MachineTester,
    tester_product: ProductTester,
):
    error: str = "Machine not found"
    test1 = tester_time_stamp.get_all_stocks_time_stamps(1)
    assert test1.json == {"Error": error}
    tester_product.post_product_add("test_name1", "100")
    tester_product.post_product_add("test_name2", "102")
    tester_machine.post_machine_add("test_name1", "test_location", "(1:20),(2:30)")
    tester_machine.post_machine_add_without_pid("test_name2", "test2_location")
    test2 = tester_time_stamp.get_all_stocks_time_stamps(1)
    first_time_stamp = test2.json[0]
    assert first_time_stamp["vending_machine_id"] == 1
    assert first_time_stamp["product_id"] == 1
    assert first_time_stamp["quantity"] == 20
    test3 = tester_time_stamp.get_all_stocks_time_stamps(2)
    assert test3.json == []


def test_get_products_time_stamps(
    tester_time_stamp: TimeStampTester,
    tester_machine: MachineTester,
    tester_product: ProductTester,
):
    error: str = "Product not found"
    test1 = tester_time_stamp.get_all_products_time_stamps(1)
    assert test1.json == {"Error": error}
    tester_product.post_product_add("test_name1", "100")
    tester_product.post_product_add("test_name2", "102")
    tester_machine.post_machine_add("test_name1", "test_location", "(1:20),(2:30)")
    tester_machine.post_machine_add_without_pid("test_name2", "test2_location")
    test2 = tester_time_stamp.get_all_products_time_stamps(1)
    first_time_stamp = test2.json[0]
    assert first_time_stamp["product_id"] == 1
    assert first_time_stamp["quantity"] == 20
    test3 = tester_time_stamp.get_all_products_time_stamps(2)
    second_time_stamp = test3.json[0]
    assert second_time_stamp["product_id"] == 2
    assert second_time_stamp["quantity"] == 30
