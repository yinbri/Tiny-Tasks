
def test_create_task(client):

    resp = client.post("/users/", json={"name": "Test User"})
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    response = client.post("/tasks/", json={
        "title":"Test Task",
        "user_id":user_id,
    })

    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["user_id"] == user_id
    assert data["completed"] is False


def test_create_task_for_missing_user(client):
    
    response = client.post("/tasks/", json={
        "user_id":9999,
        "title":"Ghost Task"
    })

    assert response.status_code == 404

def test_list_tasks(client):

    resp = client.post("/users/", json={"name": "Test User"})
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    create_task = client.post("/tasks/", json={
        "title":"Test Task",
        "user_id":user_id,
    })

    assert create_task.status_code == 201

    response = client.get("/tasks/")
    assert response.status_code == 200
    assert any(task["title"] == "Test Task" and task["user_id"] == user_id for task in response.json())

def test_list_user_tasks(client):

    resp_a = client.post("/users/", json={"name": "User A"})
    assert resp_a.status_code == 201
    a_id = resp_a.json()["id"]

    create_task_a = client.post("/tasks/", json={
        "title":"Task A",
        "user_id":a_id,
    })

    create_task_a_1 = client.post("/tasks/", json={
        "title":"Task A 1",
        "user_id":a_id,
    })

    assert create_task_a.status_code == 201
    assert create_task_a_1.status_code == 201

    resp_b = client.post("/users/", json={"name": "User B"})
    assert resp_b.status_code == 201
    b_id = resp_b.json()["id"]

    create_task_b = client.post("/tasks/", json={
        "title":"Task B",
        "user_id":b_id,
    })

    create_task_b_1 = client.post("/tasks/", json={
        "title":"Task B 1",
        "user_id":b_id,
    })

    assert create_task_b.status_code == 201
    assert create_task_b_1.status_code == 201

    response = client.get(f"/users/{a_id}/tasks/")
    assert all(task["user_id"]==a_id for task in response.json())
    assert not any(task["user_id"]==b_id for task in response.json())

def test_empty_title(client):
    response = client.post("/users/", json={"name":"Test User"})
    user_id = response.json()["id"]

    assert response.status_code == 201

    create_task = client.post("/tasks/", json={"user_id":user_id, "title":""})
    assert create_task.status_code == 422

def test_too_long_title(client):
    response = client.post("/users/", json={"name":"Test User"})
    user_id = response.json()["id"]

    assert response.status_code == 201

    create_task = client.post("/tasks/", json={"user_id":user_id, "title":'a'*202})
    assert create_task.status_code == 422

def test_wrong_task_type(client):
    create_task = client.post("/tasks/", json={"user_id":"abc", "title":123})
    assert create_task.status_code == 422
