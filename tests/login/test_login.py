import requests
from tests.config.settings import *
from tests.fixtures.usuario import *

def test_login_success(usuario_existente_admin):
    payload = {
        "email": f"{usuario_existente_admin['email']}",
        "password": f"{usuario_existente_admin['password']}"
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body
    assert isinstance(body["authorization"], str)

def test_login_com_senha_errada(usuario_existente_admin):
    payload = {
        "email": f"{usuario_existente_admin['email']}",
        "password": "senha_errada"
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Email e/ou senha inválidos"

def test_login_com_email_inexistente(usuario_existente_admin):
    payload = {
        "email": "emailinexistente@teste.com",
        "password": f"{usuario_existente_admin['password']}"
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Email e/ou senha inválidos"

def test_login_com_email_ausente_no_body(usuario_existente_admin):
    payload = {
        "email": "",
        "password": f"{usuario_existente_admin['password']}"
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["email"] == "email não pode ficar em branco"

def test_login_com_senha_ausente_no_body(usuario_existente_admin):
    payload = {
        "email": f"{usuario_existente_admin['email']}",
        "password": ""
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["password"] == "password não pode ficar em branco"

def test_login_com_body_vazio(usuario_existente_admin):
    payload = {
        "email": "",
        "password": ""
    }

    response = requests.post(f"{ENDPOINT}/login", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["email"] == "email não pode ficar em branco"
    assert body["password"] == "password não pode ficar em branco"