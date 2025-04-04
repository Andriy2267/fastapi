import pytest
from app import schemas
from .database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email": "andrijcopek696@gmail.com",
                 "password": "Chopek696"}
    res = client.post("/user/", json={user_data})
    assert res.status_code == 201
    print(res.json())
    return


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/user/", json={"email": "stepan2010@gmail.com", "password": "Leleka2025"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "stepan2010@gmail.com"
    assert res.status_code == 201


def test_login_user(client):
    res = client.post(
        "/login", data={"username": "stepan2010@gmail.com", "password": "Leleka2025"})
    print(res.json())
    assert res.status_code == 200