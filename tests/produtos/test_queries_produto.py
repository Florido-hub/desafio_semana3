from tests.fixtures.products import *
from tests.fixtures.auth_token import *


def test_can_get_product():
    response = requests.get(f"{ENDPOINT}/produtos")
    assert response.status_code == 200

def test_get_product_by_id(produto_existente):
    response = requests.get(f"{ENDPOINT}/produtos/{produto_existente['_id']}")
    assert response.status_code == 200