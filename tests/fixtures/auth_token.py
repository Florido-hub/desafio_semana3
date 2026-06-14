import pytest
import requests

from tests.config.settings import *


@pytest.fixture
def auth_token():
    payload = {
        "email": "fulano@qa.com",
        "password": "teste"
    }
    response = requests.post(
        f"{ENDPOINT}/login",json=payload
    )
    assert response.status_code == 200
    return response.json()["authorization"]