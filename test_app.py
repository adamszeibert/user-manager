import pytest
from flask import Flask
from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_create_user(client):
    response = client.post('/users', json={
        'name': 'Teszt Elek',
        'email': 'teszt.elek@gmail.com',
        'password': 'Password1'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Teszt Elek'
    assert data['email'] == 'teszt.elek@gmail.com'
    assert 'password' in data

def test_login(client):
    response = client.post('/login', json={
        'email': 'teszt.elek@gmail.com',
        'password': 'Password1'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert data['user']['email'] == 'teszt.elek@gmail.com'

def test_get_user(client):
    response = client.get('/users/teszt.elek@gmail.com')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Teszt Elek'
    assert data['email'] == 'teszt.elek@gmail.com'

def test_update_user(client):
    response = client.put('/users/teszt.elek@gmail.com', json={
        'name': 'Teszt Elek Updated',
        'email': 'teszt.elek@gmail.com',
        'password': 'Password2'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Teszt Elek Updated'
    assert data['email'] == 'teszt.elek@gmail.com'

def test_delete_user(client):
    response = client.delete('/users/teszt.elek@gmail.com')
    assert response.status_code == 204