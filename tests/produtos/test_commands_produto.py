import requests
from tests.fixtures.products import *
from tests.fixtures.auth_token import *


def test_can_create_product(auth_token):
    payload = {
        "nome": f"Produto{int(time.time()*100)}",
        "preco": 470,
        "descricao": "Produto de teste",
        "quantidade": 381,
    }

    headers = {"Authorization": auth_token}

    response = requests.post(f"{ENDPOINT}/produtos", headers=headers, json=payload)
    assert response.status_code == 201

    body = response.json()
    assert body["message"] == "Cadastro realizado com sucesso"
    assert isinstance(body["_id"], str)

    produto_id = body["_id"]
    requests.delete(f"{ENDPOINT}/produtos/{produto_id}", headers=headers)


def test_can_update_product(auth_token, produto_existente):
    payload = {
        "nome": f"produto {int(time.time()*100)}",
        "preco": 200,
        "descricao": "produto de teste alterado",
        "quantidade": 100,
    }

    headers = {"Authorization": auth_token}

    response = requests.put(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers, json=payload)
    assert response.status_code in [200,201]

    body = response.json()
    assert body["message"] == "Registro alterado com sucesso"


def test_can_delete_product(auth_token, produto_existente):
    headers = {"Authorization": auth_token}

    response = requests.delete(f"{ENDPOINT}/produtos/{produto_existente['_id']}", headers=headers)
    assert response.status_code == 200

    body = response.json()
    mensagem = ["Registro excluído com sucesso","Nenhum registro excluído"]
    assert body["message"] in mensagem