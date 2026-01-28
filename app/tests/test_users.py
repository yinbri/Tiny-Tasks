
def test_create_user(client):
    response = client.post("/users/", json={"name": "Allan"})
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "Allan"
    assert "id" in data
    assert isinstance(data["id"], int)

def test_create_wrong_type_user(client):
    response = client.post("/users/", json={"name": 123})
    
    assert response.status_code == 422

def test_list_users(client):
    response = client.post("/users/", json={"name": "Bob"})
    assert response.status_code == 201


    list_users = client.get("/users/")

    assert list_users.status_code == 200

    data = list_users.json()
    assert isinstance(data, list)
    assert any(user["name"] == 'Bob' for user in data)
    assert len(data) >= 1


def test_create_user_invalid(client):
    response = client.post("/users/", json={"name":""})
    
    assert response.status_code == 422

def test_delete_user(client):
    response = client.post("/users/", json={"name": "Allan"})
    assert response.status_code == 201
    user_id = response.json()["id"]

    delete_user = client.delete(f"/users/{user_id}/")
    assert delete_user.status_code == 204

    list_users = client.get("/users/")
    assert list_users.status_code == 200
    data = list_users.json()
    assert all(user["id"] != user_id for user in data)

    delete_again = client.delete(f"/users/{user_id}/")
    assert delete_again.status_code == 404