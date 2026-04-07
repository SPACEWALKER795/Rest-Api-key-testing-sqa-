import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Leanne Graham"}

@pytest.fixture
def sample_post():
    return {"title": "Test Post", "body": "Hello world", "userId": 1}

@pytest.fixture
def invalid_user_id():
    return 99999