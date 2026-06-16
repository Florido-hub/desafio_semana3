import random

import pytest
import time

@pytest.fixture
def sufixo():
    return f"{int(time.time())*100 + random.randint(1, 1000)}"