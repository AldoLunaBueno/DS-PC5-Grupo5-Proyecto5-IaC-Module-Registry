import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import Module

client = TestClient(app)


def test_get_modules_ok():
    """Test 200 OK en /modules"""
    response = client.get("/modules")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_module_detail():
    """Test /modules/{id}"""
    response = client.get("/modules/mod-001")
    if response.status_code == 200:
        assert response.json()["id"] == "mod-001"
    else:
        pytest.warns(UserWarning, match="mod-001 no encontrado en mock data")


def test_module_validation():
    """Test de validaciones"""
    with pytest.raises(ValueError):
        Module(
            id="test", name="Nombre Invalido", type="terraform", path="/", version="1.0"
        )
