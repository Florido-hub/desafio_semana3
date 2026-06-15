import requests
import pytest
from tests.fixtures.products import *
from tests.fixtures.usuario import *
from tests.config.settings import *
from tests.fixtures.auth_token import *

def test_criar_carrinho_sucess(produto_existente, auth_token):
    headers = {"Authorization": auth_token}

    cart_payload = {
        "produtos": [
            {
                "idProduto": produto_existente["_id"],
                "quantidade": 1
            }
        ]
    }
    carrinho_criado = False
    try:
        response = requests.post(f"{ENDPOINT}/carrinhos", headers=headers,json=cart_payload)
        assert response.status_code == 201

        body = response.json()
        assert body["message"] == "Cadastro realizado com sucesso"
        assert isinstance(body['_id'], str)
        carrinho_criado = True

    finally:
        if carrinho_criado:
            requests.delete(f"{ENDPOINT}/carrinhos/cancelar-compra", headers=headers)
