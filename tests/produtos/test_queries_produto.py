from tests.fixtures.products import *
from tests.fixtures.auth_token import *


def test_can_get_product():
    response = requests.get(f"{ENDPOINT}/produtos")
    assert response.status_code == 200

def test_get_product_by_id(produto_existente):
    response = requests.get(f"{ENDPOINT}/produtos/{produto_existente['_id']}")
    assert response.status_code == 200

def test_get_product_by_id_inexistente(produto_existente):
    response = requests.get(f"{ENDPOINT}/produtos/0000000000000000")
    assert response.status_code == 400

    body = response.json()
    assert body['message'] == "Produto não encontrado"

def test_get_product_parametro_nome(produto_existente):
    response = requests.get(f"{ENDPOINT}/produtos", params={"nome": produto_existente["nome"]})
    assert response.status_code == 200

    body = response.json()
    assert body["quantidade"] >= 1
    for produto in body["produtos"]:
        assert produto["nome"] == produto_existente["nome"]