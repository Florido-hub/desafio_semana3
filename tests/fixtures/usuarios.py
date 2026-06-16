import random

import pytest
import requests
import time

from tests.config.constants import ENDPOINT

@pytest.fixture
def usuario_existente_admin():
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"fulano {sufixo}",
        "email": f"fulano{sufixo}@email.com",
        "password": "1234",
        "administrador": "true"
    }

    response = requests.post(
        f"{ENDPOINT}/usuarios", json=payload
    )

    assert response.status_code == 201

    usuario_id = response.json()["_id"]

    yield {
        "_id": usuario_id,
        **payload
    }

    requests.delete(
        f"{ENDPOINT}/usuarios/{usuario_id}"
    )


@pytest.fixture
def usuario_existente_no_admin():
    sufixo = f"{int(time.time()) * 100 + random.randint(1, 1000)}"
    payload = {
        "nome": f"beltrano {sufixo}",
        "email": f"beltrano{sufixo}@email.com",
        "password": "1234",
        "administrador": "false"
    }

    response = requests.post(
        f"{ENDPOINT}/usuarios", json=payload
    )

    assert response.status_code == 201

    usuario_id = response.json()["_id"]

    yield {
        "_id": usuario_id,
        **payload
    }

    requests.delete(
        f"{ENDPOINT}/usuarios/{usuario_id}"
    )
