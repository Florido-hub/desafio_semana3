import pytest
import requests

from tests.config.constants import *
from tests.fixtures.usuarios import *


@pytest.fixture
def auth_token():
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": "login user",
        "email": f"login{sufixo}@email.com",
        "password": "1234",
        "administrador": "true"
    }

    requests.post(f"{ENDPOINT}/usuarios", json=payload)

    response = requests.post(f"{ENDPOINT}/login", json={
        "email": payload["email"],
        "password": payload["password"]
    })

    assert response.status_code == 200

    return response.json()["authorization"]

@pytest.fixture
def auth_token_no_admin(usuario_existente_no_admin):
    payload = {
        "email": usuario_existente_no_admin["email"],
        "password": usuario_existente_no_admin["password"]
    }
    response = requests.post(
        f"{ENDPOINT}/login", json=payload
    )
    assert response.status_code == 200
    return response.json()["authorization"]