import random

import pytest
import requests
import time
from tests.config.constants import *


def test_criar_produto_success(auth_token):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 201

    body = response.json()
    assert body["message"] == "Cadastro realizado com sucesso"
    assert isinstance(body["_id"], str)

    produto_id = body["_id"]
    requests.delete(f"{ENDPOINT}/produtos/{produto_id}", headers=headers)


def test_criar_produto_sem_header_de_autenticacao():
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    response = requests.post(f"{ENDPOINT}/produtos", json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

def test_criar_produto_com_token_invalido():
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    header = {"Authorization": "Token invalido ou expirado"}

    response = requests.post(f"{ENDPOINT}/produtos", headers=header,json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

def test_criar_produto_sem_admin(auth_token_no_admin):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token_no_admin}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 403

    body = response.json()
    assert body["message"] == "Rota exclusiva para administradores"

def test_criar_produto_sem_nome(auth_token, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": "",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['nome'] == "nome não pode ficar em branco"

def test_criar_produto_sem_preco(auth_token, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": "",
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['preco'] == "preco deve ser um número"

def test_criar_produto_preco_negativo(auth_token, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": -10,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['preco'] == "preco deve ser um número positivo"

def test_criar_produto_quantidade_negativa(auth_token, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": -100,
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['quantidade'] == "quantidade deve ser maior ou igual a 0"

def test_atualizar_produto_success(auth_token, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": produto_existente["nome"],
        "preco": sufixo,
        "descricao": produto_existente["descricao"],
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token}

    response = requests.put(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers, json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["message"] == "Registro alterado com sucesso"

def test_atualizar_produto_inexistente(auth_token, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token}

    fake_id = "0000000000000000"

    response = requests.put(f"{ENDPOINT}/produtos/{fake_id}", headers=headers, json=payload)
    assert response.status_code == 201

    body = response.json()
    assert body["message"] == "Cadastro realizado com sucesso"
    assert isinstance(body['_id'], str)

    produto_id = body["_id"]
    requests.delete(f"{ENDPOINT}/produtos/{produto_id}", headers=headers)

def test_atualizar_produto_sem_token(produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"Produto{sufixo}",
        "preco": sufixo,
        "descricao": "Produto de teste",
        "quantidade": sufixo,
    }

    headers = {"Authorization": "Token inválido"}

    response = requests.put(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers, json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

def test_atualizar_produto_sem_admin(auth_token_no_admin, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": produto_existente["nome"],
        "preco": sufixo,
        "descricao": produto_existente["descricao"],
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token_no_admin}

    response = requests.put(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers, json=payload)
    assert response.status_code == 403

    body = response.json()
    assert body["message"] == "Rota exclusiva para administradores"

def test_atualizar_produto_com_mesmo_nome(auth_token, produto_existente):
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": "Logitech MX Vertical",
        "preco": sufixo,
        "descricao": produto_existente["descricao"],
        "quantidade": sufixo,
    }

    headers = {"Authorization": auth_token}

    response = requests.put(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body["message"] == "Já existe produto com esse nome"

def test_deletar_produto_success(auth_token, produto_existente):
    headers = {"Authorization": auth_token}

    response = requests.delete(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers)
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso","Nenhum registro excluído"]
    assert body["message"] in mensagem

def test_deletar_produto_com_id_inexistente(auth_token, produto_existente):
    headers = {"Authorization": auth_token}
    fake_id = "0000000000000000"

    response = requests.delete(
        f"{ENDPOINT}/produtos/{fake_id}",
        headers=headers
    )
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso", "Nenhum registro excluído"]
    assert body["message"] in mensagem

def test_deletar_produto_sem_autenticacao(produto_existente):
    headers = {"Authorization": "Token inválido"}

    response = requests.delete(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

def test_deletar_produto_sem_admin(auth_token_no_admin, produto_existente):
    headers = {"Authorization": auth_token_no_admin}

    response = requests.delete(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers)
    assert response.status_code == 403

    body = response.json()
    assert body["message"] == "Rota exclusiva para administradores"