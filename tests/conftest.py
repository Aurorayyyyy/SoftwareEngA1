from dataclasses import dataclass

import pytest
from flask import Flask
from flask.testing import FlaskClient


@pytest.fixture()
def app():
    from app import create_app

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@dataclass
class Tester:
    client: FlaskClient
