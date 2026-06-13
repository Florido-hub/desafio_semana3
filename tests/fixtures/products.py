import pytest
import requests
import time

from tests.config.settings import ENDPOINT


@pytest.fixture
def produto_existente(auth_token):
    payload = {
        "nome": f"Produto {int(time.time())}",
        "preco": 100,
        "descricao": "Produto de teste",
        "quantidade": 100
    }

    response = requests.post(
        f"{ENDPOINT}/produtos",
        json=payload,
        headers={"Authorization": auth_token}
    )

    assert response.status_code == 201

    produto_id = response.json()["_id"]

    yield {
        "_id": produto_id,
        **payload
    }

    requests.delete(
        f"{ENDPOINT}/produtos/{produto_id}",
        headers={"Authorization": auth_token}
    )