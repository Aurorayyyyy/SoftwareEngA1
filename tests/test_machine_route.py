import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.conftest import Tester
from tests.test_product_route import ProductTester


@pytest.fixture
def tester_product(client: FlaskClient) -> ProductTester:
    return ProductTester(client)


class MachineTester(Tester):
    def get_all_machine(self) -> TestResponse:
        return self.client.get("/machines")

    def post_machine_add(self, name: str, location: str, pid: str) -> TestResponse:
        return self.client.post(
            "/machines/add", data={"name": name, "location": location, "pid": pid}
        )

    def post_machine_add_without_pid(self, name: str, location: str) -> TestResponse:
        return self.client.post(
            "/machines/add", data={"name": name, "location": location}
        )

    def post_machine_edit(
        self, machine_id: int, name: str, location: str, pid: str
    ) -> TestResponse:
        return self.client.post(
            f"/machines/edit/{machine_id}",
            data={"name": name, "location": location, "pid": pid},
        )

    def post_machine_edit_name_only(self, machine_id: int, name: str) -> TestResponse:
        return self.client.post(f"/machines/edit/{machine_id}", data={"name": name})

    def post_machine_edit_location_only(
        self, machine_id: int, location: str
    ) -> TestResponse:
        return self.client.post(
            f"/machines/edit/{machine_id}", data={"location": location}
        )

    def post_machine_edit_pid_only(self, machine_id: int, pid: str) -> TestResponse:
        return self.client.post(f"/machines/edit/{machine_id}", data={"pid": pid})

    def post_machine_delete(self, machine_id: int) -> TestResponse:
        return self.client.post(f"/machines/delete/{machine_id}")


@pytest.fixture()
def tester(client: FlaskClient) -> MachineTester:
    return MachineTester(client=client)


def get_all(tester: MachineTester):
    get_all_response = tester.get_all_machine()
    assert get_all_response.json == []


def test_add_machine(tester: MachineTester, tester_product: ProductTester):
    tester_product.post_product_add("test_name1", "100")
    tester_product.post_product_add("test_name2", "102")
    add_machine1 = tester.post_machine_add(
        "test_name1", "test_location", "(1:20),(2:30)"
    )
    assert add_machine1.json == {
        "id": 1,
        "name": "test_name1",
        "location": "test_location",
        "machine_products": [
            {"product_id": 1, "quantity": 20},
            {"product_id": 2, "quantity": 30},
        ],
    }
    add_machine2 = tester.post_machine_add_without_pid("test_name2", "test2_location")
    assert add_machine2.json == {
        "id": 2,
        "name": "test_name2",
        "location": "test2_location",
        "machine_products": [],
    }


def test_edit_machine(tester: MachineTester, tester_product: ProductTester):
    tester_product.post_product_add("test_name1", "100")
    tester_product.post_product_add("test_name2", "102")
    tester_product.post_product_add("test_name3", "103")
    tester.post_machine_add("test_name1", "test_location", "(1:22),(2:33)")

    edit1 = tester.post_machine_edit(1, "edit_test", "edit_location", "(1:24)")
    assert edit1.json == {
        "id": 1,
        "name": "edit_test",
        "location": "edit_location",
        "machine_products": [{"product_id": 1, "quantity": 24}],
    }
    edit2 = tester.post_machine_edit_name_only(1, "edit_name_test")
    assert edit2.json == {
        "id": 1,
        "name": "edit_name_test",
        "location": "edit_location",
        "machine_products": [{"product_id": 1, "quantity": 24}],
    }
    edit3 = tester.post_machine_edit_location_only(1, "new_location")
    assert edit3.json == {
        "id": 1,
        "name": "edit_name_test",
        "location": "new_location",
        "machine_products": [{"product_id": 1, "quantity": 24}],
    }
    edit4 = tester.post_machine_edit_pid_only(1, "")
    assert edit4.json == {
        "id": 1,
        "name": "edit_name_test",
        "location": "new_location",
        "machine_products": [],
    }
    edit5 = tester.post_machine_edit_pid_only(1, "(3:20)")
    assert edit5.json == {
        "id": 1,
        "name": "edit_name_test",
        "location": "new_location",
        "machine_products": [{"product_id": 3, "quantity": 20}],
    }
    edit6 = tester.post_machine_edit(10, "edit_test", "edit_location", "(1:20)")
    assert edit6.json == {"Error": "Machine not found"}


def test_delete_machine(tester: MachineTester, tester_product: ProductTester):
    tester_product.post_product_add("test_name1", "100")
    tester_product.post_product_add("test_name2", "102")
    tester.post_machine_add("test_name1", "test1_location", "(1:40),(2:60)")
    tester.post_machine_add("test_name2", "test2_location", "(1:20)")
    tester.post_machine_add_without_pid("test_name3", "test3_location")

    message: str = "Delete Successful"
    delete_tester1 = tester.post_machine_delete(1)
    assert delete_tester1.json == {"Message": message}
    delete_tester2 = tester.post_machine_delete(2)
    assert delete_tester2.json == {"Message": message}
    delete_tester3 = tester.post_machine_delete(3)
    assert delete_tester3.json == {"Message": message}

    get_all_response = tester.get_all_machine()
    assert get_all_response.json == []

    error: str = "Machine not found"
    delete_tester1 = tester.post_machine_delete(1)
    assert delete_tester1.json == {"Error": error}
    delete_tester2 = tester.post_machine_delete(2)
    assert delete_tester2.json == {"Error": error}
    delete_tester3 = tester.post_machine_delete(3)
    assert delete_tester3.json == {"Error": error}
