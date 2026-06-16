import random

import pytest
import requests
import time
from tests.config.constants import *

def test_criar_usuario_success():
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"fulano{sufixo}",
        "email": f"fulano{sufixo}@email.com",
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

def test_criar_usuario_com_email_em_uso(usuario_existente_admin):
    payload = {
        "nome": "nome de usuario",
        "email": usuario_existente_admin["email"],
        "password": "1234",
        "administrador": "true"
    }

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["message"] == "Este email já está sendo usado"

@pytest.mark.parametrize("campo,expected", [
    ("nome", "nome é obrigatório"),
    ("email", "email é obrigatório"),
    ("password", "password é obrigatório"),
    ("administrador", "administrador é obrigatório"),
])
def test_criar_usuario_com_body_vazio(campo, expected):
    payload = {
    }

    payload[campo] = ""

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 400

def test_criar_usuario_com_email_inválido():
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"fulano{sufixo}",
        "email": f"fulano{sufixo}",
        "password": "1234",
        "administrador": "true"
    }

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["email"] == "email deve ser um email válido"


def test_atualizar_usuario_success(usuario_existente_admin):
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

def test_atualizar_usuario_inexistente():
    update_payload = {
        "nome": "Nome atualizado",
        "email": "email@atualizado.com",
        "password": "teste",
        "administrador": "true"
    }

    fake_id = "0000000000000000"

    response = requests.put(
        f"{ENDPOINT}/usuarios/{fake_id}", json=update_payload
    )
    assert response.status_code == 201

    body = response.json()
    assert body["message"] == "Cadastro realizado com sucesso"
    assert isinstance(body["_id"], str)

    usuario_id = body["_id"]
    requests.delete(f"{ENDPOINT}/usuarios/{usuario_id}")

def test_atualizar_usuario_com_email_em_uso(usuario_existente_admin, usuario_existente_no_admin):
    payload_update = {
        "nome": "nome atualizado",
        "email": usuario_existente_no_admin["email"],
        "password": "1234",
        "administrador": "true"
    }

    response = requests.put(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}", json=payload_update)
    assert response.status_code == 400

    body = response.json()
    assert body["message"] == "Este email já está sendo usado"

def test_atualizar_usuario_com_campo_obrigatorio_ausente(usuario_existente_admin):
    payload = {
        "nome": "",
        "email": "fulano@qa.com",
        "password": "1234",
        "administrador": "true"
    }

    response = requests.put(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["nome"] == "nome não pode ficar em branco"


def test_deletar_usuario_success(usuario_existente_admin):
    response = requests.delete(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}")
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso", "Nenhum registro excluído"]
    assert body["message"] in mensagem

#Olha aí o caso de não encontrar e retornar status 200, professor
def test_deletar_usuario_com_id_inexistente():
    fake_id = "000000000000000000000000"

    response = requests.delete(
        f"{ENDPOINT}/usuarios/{fake_id}"
    )
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso", "Nenhum registro excluído"]
    assert body["message"] in mensagem

