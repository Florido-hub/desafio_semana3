import pytest
import requests
import time
from tests.config.settings import *
from tests.fixtures.usuario import *

def test_create_user():
    payload = {
        "nome": f"fulano{int(time.time()*100)}",
        "email": f"fulano{int(time.time()*100)}@email.com",
        "password": "1234",
        "administrador": "true"
    }

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 201

    body = response.json()
    assert body["message"] == "Cadastro realizado com sucesso"
    assert isinstance(body["_id"], str)

    user_id = body["_id"]
    requests.delete(f"{ENDPOINT}/usuarios/{user_id}")

def test_create_user_email_already_registered(usuario_existente):
    payload = {
        "nome": f"fulano{int(time.time()*100)}",
        "email": usuario_existente["email"],
        "password": "1234",
        "administrador": "true"
    }

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["message"] == "Este email já está sendo usado"
