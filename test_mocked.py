import pytest, allure
pytestmark = [allure.label("suite", "Mocked Tests")]
from unittest.mock import patch, Mock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import get_user, create_post

@allure.title("Mocked GET returns fake user data")
@allure.description("Uses unittest.mock to fake the API response — verifies test runs without real internet.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_get_user_mocked():
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"id": 1, "name": "Fake User", "email": "fake@test.com"}
    with patch("api_client.requests.get", return_value=mock_resp):
        with allure.step("Call get_user with mocked response"):
            response = get_user(1)
        with allure.step("Verify mocked status and name"):
            assert response.status_code == 200
            assert response.json()["name"] == "Fake User"

@allure.title("Mocked server error returns 500")
@allure.description("Simulates a server error response to verify error handling works correctly.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_api_server_error_mocked():
    mock_resp = Mock()
    mock_resp.status_code = 500
    mock_resp.json.return_value = {"error": "Internal server error"}
    with patch("api_client.requests.get", return_value=mock_resp):
        with allure.step("Call get_user with 500 error mocked"):
            response = get_user(1)
        with allure.step("Verify status code is 500"):
            assert response.status_code == 500

@allure.title("Mocked POST creates post successfully")
@allure.description("Verifies create_post works correctly using a mocked 201 response.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_create_post_mocked():
    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"id": 101, "title": "Test", "body": "Body", "userId": 1}
    with patch("api_client.requests.post", return_value=mock_resp):
        with allure.step("Call create_post with mocked response"):
            response = create_post("Test", "Body", 1)
        with allure.step("Verify status 201 and ID 101"):
            assert response.status_code == 201
            assert response.json()["id"] == 101