import pytest
import requests
from tests.config.constants import *
from jsonschema import validate
from tests.fixtures.utils.usuario_schema import *


@pytest.mark.list
@pytest.mark.list_user
def test_listar_usuario():
    response = requests.get(f"{ENDPOINT}/usuarios")
    assert response.status_code == 200

    body = response.json()
    validate(instance=body, schema=USUARIO_SCHEMA)
    assert body["quantidade"] == len(body["usuarios"])

@pytest.mark.list
@pytest.mark.list_user
def test_listar_usuario_pelo_id(usuario_existente_admin):
    response = requests.get(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}")
    assert response.status_code == 200

    body = response.json()
    validate(instance=body, schema=USUARIO_SCHEMA_ID)
    assert body["_id"] == usuario_existente_admin["_id"]

@pytest.mark.list
@pytest.mark.list_user
def test_listar_usuario_com_id_inexistente():
    # ID com formato válido (16 chars alfanuméricos) mas inexistente
    response = requests.get(f"{ENDPOINT}/usuarios/0000000000000000")
    assert response.status_code == 400
    assert response.json()["message"] == "Usuário não encontrado"
