import pytest, sys, os, allure
pytestmark = [allure.label("suite", "Negative Tests")]
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import get_user, create_post

@allure.title("Non-existent user returns 404")
@allure.description("Verifies that requesting a user with a very high ID returns HTTP 404.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_user_not_found(invalid_user_id):
    with allure.step(f"Send GET request for user {invalid_user_id}"):
        response = get_user(invalid_user_id)
    with allure.step("Verify status code is 404"):
        assert response.status_code == 404

@allure.title("Invalid user IDs return error status")
@allure.description("Parameterized boundary test using IDs 0, -1, and -999 which should all return errors.")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.negative
@pytest.mark.parametrize("bad_id", [0, -1, -999])
def test_invalid_user_ids(bad_id):
    with allure.step(f"Send GET request with invalid ID {bad_id}"):
        response = get_user(bad_id)
    with allure.step("Verify error status code returned"):
        assert response.status_code in [400, 404]

@allure.title("Post with empty title is handled gracefully")
@allure.description("Verifies the API handles a POST request with an empty title without crashing.")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.negative
def test_create_post_empty_title():
    with allure.step("Send POST with empty title"):
        response = create_post("", "Some body text", 1)
    with allure.step("Verify response is 400 or 201"):
        assert response.status_code in [400, 201]

@allure.title("Post with empty body is handled gracefully")
@allure.description("Verifies the API handles a POST request with an empty body without crashing.")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.negative
def test_create_post_empty_body():
    with allure.step("Send POST with empty body"):
        response = create_post("My title", "", 1)
    with allure.step("Verify response is 400 or 201"):
        assert response.status_code in [400, 201]