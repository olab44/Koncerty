import pytest
from fastapi.testclient import TestClient
from main import app


def test_example():
    assert 1 + 1 == 2
	

# def test_fail():
#     assert 1+1==3


@pytest.fixture
def client():
    return TestClient(app)


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
    assert "Content-Security-Policy" in response.headers


def test_logging_middleware(client, capsys):
    client.get("/")
    
    captured = capsys.readouterr()
    assert "Incoming request" in captured.out


def test_csp_middleware(client):
    response = client.get("/")
    assert "Content-Security-Policy" in response.headers
    assert response.headers["Content-Security-Policy"] == "default-src *;"

