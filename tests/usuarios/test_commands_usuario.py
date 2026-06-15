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

def test_create_user_email_em_uso(usuario_existente_admin):
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

def test_create_user_sem_body():
    payload = {
    }

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["nome"] == "nome é obrigatório"
    assert body["email"] == "email é obrigatório"
    assert body["password"] == "password é obrigatório"
    assert body["administrador"] == "administrador é obrigatório"

def test_create_user_email_formato_inválido():
    payload = {
        "nome": f"fulano{int(time.time() * 100)}",
        "email": f"fulano{int(time.time() * 100)}",
        "password": "1234",
        "administrador": "true"
    }

    response = requests.post(f"{ENDPOINT}/usuarios", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["email"] == "email deve ser um email válido"


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

def test_update_user_inexistente():
    update_payload = {
        "nome": "Nome atualizado",
        "email": "email@atualizado.com",
        "password": "teste",
        "administrador": "true"
    }

    fake_id = "000000000000000000000000"

    response = requests.put(
        f"{ENDPOINT}/usuarios/{fake_id}", json=update_payload
    )
    assert response.status_code == 201

    body = response.json()
    assert body["message"] == "Cadastro realizado com sucesso"
    assert isinstance(body["_id"], str)

    usuario_id = body["_id"]
    requests.delete(f"{ENDPOINT}/usuarios/{usuario_id}")

def test_update_user_email_em_uso(usuario_existente_admin):
    payload = {
        "nome": f"fulano{int(time.time()*100)}",
        "email": "fulano@qa.com",
        "password": "1234",
        "administrador": "true"
    }

    response = requests.put(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["message"] == "Este email já está sendo usado"

def test_update_user_campo_obrigatorio_ausente(usuario_existente_admin):
    payload = {
        "nome": "",
        "email": "fulano@qa.com",
        "password": "1234",
        "administrador": "true"
    }

    response = requests.put(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}", json=payload)
    assert response.status_code == 400

    body = response.json()
    print(body)


def test_delete_user_success(usuario_existente_admin):
    response = requests.delete(f"{ENDPOINT}/usuarios/{usuario_existente_admin['_id']}")
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso", "Nenhum registro excluído"]
    assert body["message"] in mensagem

#Olha aí o caso de não encontrar e retornar status 200, professor
def test_delete_user_id_inexistente():
    fake_id = "000000000000000000000000"

    response = requests.delete(
        f"{ENDPOINT}/usuarios/{fake_id}"
    )
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso", "Nenhum registro excluído"]
    assert body["message"] in mensagem

