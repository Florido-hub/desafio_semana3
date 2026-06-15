import pytest
import requests
import time

from tests.config.settings import ENDPOINT

@pytest.fixture
def usuario_existente_admin():
    payload = {
        "nome": f"fulano {int(time.time())}",
        "email": f"fluano{int(time.time())}@email.com",
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
    payload = {
        "nome": f"fulano {int(time.time())}",
        "email": f"fluano{int(time.time())}@email.com",
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
