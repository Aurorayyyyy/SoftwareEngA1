from dataclasses import dataclass

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import reset_database


@pytest.fixture()
def app():
    from app import create_app

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    app.config.update(
        {
            "WTF_CSRF_CHECK_DEFAULT": False,
        }
    )
    reset_database(app)

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@dataclass
class Tester:
    client: FlaskClient
