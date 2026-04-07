import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def get_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    return response

def get_all_users():
    response = requests.get(f"{BASE_URL}/users")
    return response

def get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")
    return response

def get_post(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    return response

def create_post(title, body, user_id):
    response = requests.post(f"{BASE_URL}/posts", json={
        "title": title,
        "body": body,
        "userId": user_id
    })
    return response

def delete_post(post_id):
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    return response