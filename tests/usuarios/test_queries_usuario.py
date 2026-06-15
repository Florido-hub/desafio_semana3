import pytest
import requests
from tests.config.settings import *
from tests.fixtures.auth_token import *
from tests.fixtures.usuario import *

def test_can_get_users():
    response = requests.get(f"{ENDPOINT}/usuarios")
    assert response.status_code == 200

def test_get_users_by_id(usuario_existente_admin):
    response = requests.get(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}")
    assert response.status_code == 200

    # TODO: melhorar usando validação de schema (jsonschema)
    body = response.json()
    assert body["nome"] == usuario_existente_admin["nome"]
    assert body["email"] == usuario_existente_admin["email"]
    assert body["password"] == usuario_existente_admin["password"]
    assert body["administrador"] == usuario_existente_admin["administrador"]
    assert body["_id"] == usuario_existente_admin["_id"]


def test_get_users_by_id_invalid_format():
    # ID com formato inválido — a API rejeita com erro de validação
    response = requests.get(f"{ENDPOINT}/usuarios/usuarioinexistente")
    assert response.status_code == 400

def test_get_users_by_id_not_found():
    # ID com formato válido (16 chars alfanuméricos) mas inexistente
    response = requests.get(f"{ENDPOINT}/usuarios/0000000000000000")
    assert response.status_code == 400
    assert response.json()["message"] == "Usuário não encontrado"

def test_get_user_filter_by_admin_true():
    response = requests.get(f"{ENDPOINT}/usuarios", params={"administrador": "true"})
    assert response.status_code == 200

    body = response.json()
    assert body["quantidade"] >= 1
    for usuario in body["usuarios"]:
        assert usuario["administrador"] == "true"

def test_get_user_filter_by_admin_false(usuario_existente_no_admin):
    response = requests.get(f"{ENDPOINT}/usuarios", params={"administrador": "false"})
    assert response.status_code == 200

    body = response.json()
    assert body["quantidade"] >= 1
    for usuario in body["usuarios"]:
        assert usuario["administrador"] == "false"
