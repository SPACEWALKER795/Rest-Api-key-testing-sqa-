import pytest, time, sys, os, allure
pytestmark = [allure.label("suite", "Performance Tests")]
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import get_user, get_all_posts

@allure.title("Single user request responds within 3 seconds")
@allure.description("Performance test — measures response time for GET /users/1 and fails if over 3 seconds.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_single_user_response_time():
    with allure.step("Record start time"):
        start = time.time()
    with allure.step("Send GET request to /users/1"):
        response = get_user(1)
    with allure.step("Calculate duration and verify under 3s"):
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 3.0, f"Too slow: {duration:.2f}s"
        print(f"\nResponse time: {duration:.3f}s")

@allure.title("All posts request responds within 5 seconds")
@allure.description("Performance test — measures response time for GET /posts and fails if over 5 seconds.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_all_posts_response_time():
    with allure.step("Record start time"):
        start = time.time()
    with allure.step("Send GET request to /posts"):
        response = get_all_posts()
    with allure.step("Calculate duration and verify under 5s"):
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 5.0, f"Too slow: {duration:.2f}s"
        print(f"\nResponse time: {duration:.3f}s")