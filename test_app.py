import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_file_upload(client):
    data = {'file': (open('test_file.txt', 'rb'), 'test_file.txt')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    assert 'file_id' in response.json

def test_invalid_download(client):
    response = client.get('/download/nonexistent')
    assert response.status_code == 404
