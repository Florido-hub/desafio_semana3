import pytest
import requests

from tests.config.settings import *
from tests.fixtures.usuario import *


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

@pytest.fixture
def auth_token_dinamico(usuario_existente_admin):
    payload = {
        "email": usuario_existente_admin["email"],
        "password": usuario_existente_admin["password"]
    }
    response = requests.post(
        f"{ENDPOINT}/login", json=payload
    )
    assert response.status_code == 200
    return response.json()["authorization"]

@pytest.fixture
def auth_token_dinamico_sem_admin(usuario_existente_no_admin):
    payload = {
        "email": usuario_existente_no_admin["email"],
        "password": usuario_existente_no_admin["password"]
    }
    response = requests.post(
        f"{ENDPOINT}/login", json=payload
    )
    assert response.status_code == 200
    return response.json()["authorization"]