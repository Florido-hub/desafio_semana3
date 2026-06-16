import pytest
import requests
import time

from tests.config.constants import ENDPOINT
from tests.fixtures.auth_token import *


@pytest.fixture
def produto_existente(auth_token):
    payload = {
        "nome": f"Produto {int(time.time())}",
        "preco": 100,
        "descricao": "Produto de teste",
        "quantidade": 100
    }

    headers = {"Authorization": auth_token}

    response = requests.post(
        f"{ENDPOINT}/produtos",json=payload, headers=headers
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