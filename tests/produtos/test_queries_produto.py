import pytest
import requests
from tests.config.constants import *

def test_listar_produto():
    response = requests.get(f"{ENDPOINT}/produtos")
    assert response.status_code == 200

def test_listar_produto_pelo_id(produto_existente):
    response = requests.get(f"{ENDPOINT}/produtos/{produto_existente['_id']}")
    assert response.status_code == 200

def test_listar_produto_com_id_inexistente(produto_existente):
    response = requests.get(f"{ENDPOINT}/produtos/0000000000000000")
    assert response.status_code == 400

    body = response.json()
    assert body['message'] == "Produto não encontrado"

def test_listar_produto_com_parametro_nome(produto_existente):
    response = requests.get(f"{ENDPOINT}/produtos", params={"nome": produto_existente["nome"]})
    assert response.status_code == 200

    body = response.json()
    assert body["quantidade"] >= 1
    for produto in body["produtos"]:
        assert produto["nome"] == produto_existente["nome"]