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

def test_create_user_email_already_registered(usuario_existente_admin):
    payload = {
        "nome": f"fulano{int(time.time()*100)}",
        "email": usuario_existente_admin["email"],
        "password": "1234",
        "administrador": "true"
    }

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["message"] == "Este email já está sendo usado"


def test_update_user(usuario_existente_admin):
    update_payload = {
        "nome": "Nome atualizado",
        "email": usuario_existente_admin["email"],
        "password": usuario_existente_admin["password"],
        "administrador": usuario_existente_admin["administrador"]
    }

    response = requests.put(
        f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}", json=update_payload
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Registro alterado com sucesso"

    # Verifica que a alteração foi persistida
    get_response = requests.get(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}")
    assert get_response.status_code == 200
    assert get_response.json()["nome"] == "Nome atualizado"


def test_delete_user_success(usuario_existente_admin):
    response = requests.delete(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}")
    assert response.status_code == 200

    body = response.json()
    assert body["message"] == "Registro excluído com sucesso"