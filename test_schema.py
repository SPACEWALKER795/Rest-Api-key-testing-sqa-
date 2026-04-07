import pytest, sys, os, requests, allure
pytestmark = [allure.label("suite", "Schema Validation")]
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@allure.title("User response has all required fields")
@allure.description("Checks that the user object contains all 6 required fields: id, name, username, email, address, phone.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
def test_user_required_fields(base_url, sample_user):
    with allure.step("Send GET request for user"):
        response = requests.get(f"{base_url}/users/{sample_user['id']}")
    with allure.step("Verify all required fields exist"):
        data = response.json()
        for field in ["id", "name", "username", "email", "address", "phone"]:
            assert field in data, f"Missing field: {field}"

@allure.title("User field types are correct")
@allure.description("Verifies id is int, name and email are strings, and email contains @ symbol.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_user_field_types(base_url, sample_user):
    with allure.step("Send GET request for user"):
        response = requests.get(f"{base_url}/users/{sample_user['id']}")
    with allure.step("Verify field types"):
        data = response.json()
        assert isinstance(data["id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["email"], str)
    with allure.step("Verify email format"):
        assert "@" in data["email"]

@allure.title("Posts list is a non-empty array with correct fields")
@allure.description("Verifies the posts endpoint returns a list with id, title, body, and userId fields.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_posts_list_structure(base_url):
    with allure.step("Send GET request to /posts"):
        response = requests.get(f"{base_url}/posts")
    with allure.step("Verify response is a non-empty list"):
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0
    with allure.step("Verify first post has required fields"):
        for field in ["id", "title", "body", "userId"]:
            assert field in posts[0], f"Missing field: {field}"