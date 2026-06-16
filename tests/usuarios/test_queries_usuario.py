import pytest
import requests
from tests.config.constants import *

def test_listar_usuario():
    response = requests.get(f"{ENDPOINT}/usuarios")
    assert response.status_code == 200

def test_listar_usuario_pelo_id(usuario_existente_admin):
    response = requests.get(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}")
    assert response.status_code == 200

    # TODO: melhorar usando validação de schema (jsonschema)
    body = response.json()
    assert body["nome"] == usuario_existente_admin["nome"]
    assert body["email"] == usuario_existente_admin["email"]
    assert body["password"] == usuario_existente_admin["password"]
    assert body["administrador"] == usuario_existente_admin["administrador"]
    assert body["_id"] == usuario_existente_admin["_id"]

def test_listar_usuario_com_id_inexistente():
    # ID com formato válido (16 chars alfanuméricos) mas inexistente
    response = requests.get(f"{ENDPOINT}/usuarios/0000000000000000")
    assert response.status_code == 400
    assert response.json()["message"] == "Usuário não encontrado"
