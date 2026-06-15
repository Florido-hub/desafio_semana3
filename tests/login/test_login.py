import requests
from tests.config.settings import *
from tests.fixtures.usuario import *

def test_login_success(usuario_existente):
    payload = {
        "email": f"{usuario_existente['email']}",
        "password": f"{usuario_existente['password']}"
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body
    assert isinstance(body["authorization"], str)

def test_login_fail(usuario_existente):
    payload = {
        "email": f"{usuario_existente['email']}",
        "password": "senha_errada"
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Email e/ou senha inválidos"