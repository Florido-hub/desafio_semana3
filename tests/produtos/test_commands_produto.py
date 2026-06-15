import requests
from tests.fixtures.products import *
from tests.fixtures.auth_token import *
from tests.fixtures.usuario import *


def test_can_create_product(auth_token):
    payload = {
        "nome": f"Produto{int(time.time()*100)}",
        "preco": int(time.time()*100),
        "descricao": "Produto de teste",
        "quantidade": int(time.time()*100),
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
    payload = {
        "nome": f"Produto{int(time.time() * 100)}",
        "preco": int(time.time() * 100),
        "descricao": "Produto de teste",
        "quantidade": int(time.time() * 100),
    }

    response = requests.post(f"{ENDPOINT}/produtos", json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

def test_criar_produto_com_token_invalido():
    payload = {
        "nome": f"Produto{int(time.time() * 100)}",
        "preco": int(time.time() * 100),
        "descricao": "Produto de teste",
        "quantidade": int(time.time() * 100),
    }

    header = {"Authorization": "Token invalido ou expirado"}

    response = requests.post(f"{ENDPOINT}/produtos", headers=header,json=payload)
    assert response.status_code == 401

    body = response.json()
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

def test_criar_produto_sem_admin(auth_token_dinamico_sem_admin):
    payload = {
        "nome": f"Produto{int(time.time() * 100)}",
        "preco": int(time.time() * 100),
        "descricao": "Produto de teste",
        "quantidade": int(time.time() * 100),
    }

    headers = {"Authorization": auth_token_dinamico_sem_admin}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 403

    body = response.json()
    assert body["message"] == "Rota exclusiva para administradores"

def test_criar_produto_sem_nome(auth_token, produto_existente):
    payload = {
        "nome": "",
        "preco": int(time.time() * 100),
        "descricao": "Produto de teste",
        "quantidade": int(time.time() * 100),
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['nome'] == "nome não pode ficar em branco"

def test_criar_produto_sem_preco(auth_token, produto_existente):
    payload = {
        "nome": f"Produto{int(time.time() * 100)}",
        "preco": "",
        "descricao": "Produto de teste",
        "quantidade": int(time.time() * 100),
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['preco'] == "preco deve ser um número"

def test_criar_produto_preco_negativo(auth_token, produto_existente):
    payload = {
        "nome": f"Produto{int(time.time() * 100)}",
        "preco": -10,
        "descricao": "Produto de teste",
        "quantidade": int(time.time() * 100),
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['preco'] == "preco deve ser um número positivo"

def test_criar_produto_quantidade_negativa(auth_token, produto_existente):
    payload = {
        "nome": f"Produto{int(time.time() * 100)}",
        "preco": int(time.time() * 100),
        "descricao": "Produto de teste",
        "quantidade": -100,
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 400

    body = response.json()
    assert body['quantidade'] == "quantidade deve ser maior ou igual a 0"

def test_can_update_product(auth_token, produto_existente):
    payload = {
        "nome": produto_existente["nome"],
        "preco": produto_existente["preco"],
        "descricao": produto_existente["descricao"],
        "quantidade": produto_existente["quantidade"],
    }

    headers = {"Authorization": auth_token}

    response = requests.put(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers, json=payload)
    assert response.status_code in [200]

    body = response.json()
    assert body["message"] == "Registro alterado com sucesso"


def test_can_delete_product(auth_token, produto_existente):
    headers = {"Authorization": auth_token}

    response = requests.delete(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers)
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso","Nenhum registro excluído"]
    assert body["message"] in mensagem