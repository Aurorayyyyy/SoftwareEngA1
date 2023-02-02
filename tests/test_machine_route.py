import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.conftest import Tester


class MachineTester(Tester):
    def get_all(self) -> TestResponse:
        return self.client.get("/machines")

    def post_machine_add(self, name: str, location: str, pid: str) -> TestResponse:
        return self.client.post(
            "/products/add", data={"name": name, "location": location, "pid": pid}
        )


@pytest.fixture()
def tester(client: FlaskClient) -> MachineTester:
    return MachineTester(client=client)


def test_get_all(tester: MachineTester):
    get_all_response = tester.get_all()

    print(get_all_response.json)
