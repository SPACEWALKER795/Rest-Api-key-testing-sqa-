import pytest, sys, os, allure
pytestmark = [allure.label("suite", "User Tests")]
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import get_user

@allure.title("Multiple users exist and return 200")
@allure.description("Parameterized test verifying users 1 through 5 all return HTTP 200.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
def test_multiple_users_exist(user_id):
    with allure.step(f"Send GET request for user {user_id}"):
        response = get_user(user_id)
    with allure.step("Verify status code is 200"):
        assert response.status_code == 200
    with allure.step("Verify returned ID matches requested ID"):
        assert response.json()["id"] == user_id

@allure.title("User names match expected values")
@allure.description("Verifies that specific users return their correct names from the API.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch"),
])
def test_user_names_correct(user_id, expected_name):
    with allure.step(f"Get user {user_id}"):
        response = get_user(user_id)
    with allure.step(f"Verify name is {expected_name}"):
        assert response.json()["name"] == expected_name