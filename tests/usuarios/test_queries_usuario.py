import pytest
import requests
from tests.config.settings import *
from tests.fixtures.auth_token import *
from tests.fixtures.usuario import *

def test_can_get_users():
    response = requests.get(f"{ENDPOINT}/usuarios")
    assert response.status_code == 200

def test_get_users_by_id(usuario_existente):
    response = requests.get(f"{ENDPOINT}/usuarios/{usuario_existente['_id']}")
    assert response.status_code == 200

    #Melhorar aqui usando o rolê do schema q jacques ensinou
    body = response.json()
    assert body["nome"] == usuario_existente["nome"]
    assert body["email"] == usuario_existente["email"]
    assert body["password"] == usuario_existente["password"]
    assert body["administrador"] == usuario_existente["administrador"]
    assert body["_id"] == usuario_existente["_id"]


def test_get_users_by_id_fail():
    response = requests.get(f"{ENDPOINT}/usuarios/usuarioinexistente")
    assert response.status_code == 400