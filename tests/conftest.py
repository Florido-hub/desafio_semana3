import pytest

pytest_plugins = [
    "tests.fixtures.usuarios",
    "tests.fixtures.produtos",
    "tests.fixtures.auth_token",
    "tests.fixtures.utils.sufixo"
]