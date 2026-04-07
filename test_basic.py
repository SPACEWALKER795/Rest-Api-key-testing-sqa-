import pytest, sys, os, allure
pytestmark = [allure.label("suite", "Basic API Tests")]
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import get_user, get_all_posts, create_post, delete_post

@allure.title("GET /users/1 returns success")
@allure.description("Verifies that user with ID 1 exists and the API returns HTTP 200 with correct data.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("users", "smoke")
@pytest.mark.smoke
def test_get_user_success():
    with allure.step("Send GET request to /users/1"):
        response = get_user(1)
    with allure.step("Verify status code is 200"):
        assert response.status_code == 200
    with allure.step("Verify returned ID is 1"):
        assert response.json()["id"] == 1

@allure.title("GET /posts returns full list")
@allure.description("Verifies that the posts endpoint returns HTTP 200 and a non-empty list.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("posts", "smoke")
@pytest.mark.smoke
def test_get_all_posts():
    with allure.step("Send GET request to /posts"):
        response = get_all_posts()
    with allure.step("Verify status code is 200"):
        assert response.status_code == 200
    with allure.step("Verify list is not empty"):
        assert len(response.json()) > 0

@allure.title("POST /posts creates a new post")
@allure.description("Verifies that a new post can be created and returns HTTP 201 with correct title.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("posts", "smoke")
@pytest.mark.smoke
def test_create_post():
    with allure.step("Send POST request with title Hello"):
        response = create_post("Hello", "My first post", 1)
    with allure.step("Verify status code is 201"):
        assert response.status_code == 201
    with allure.step("Verify title matches sent value"):
        assert response.json()["title"] == "Hello"

@allure.title("DELETE /posts/1 returns success")
@allure.description("Verifies that an existing post can be deleted and returns HTTP 200.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("posts", "regression")
@pytest.mark.regression
def test_delete_post():
    with allure.step("Send DELETE request to /posts/1"):
        response = delete_post(1)
    with allure.step("Verify status code is 200"):
        assert response.status_code == 200