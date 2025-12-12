import os
import json
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient
from app.main import app

QUALITY_REPORT = {
    "modules": [
        {"id": "mod-001", "type": "terraform", "result": "OK", "details": ""},
        {"id": "mod-002", "type": "k8s", "result": "WARN", "details": ""},
        {"id": "mod-003", "type": "terraform", "result": "FAIL", "details": ""}
    ],
    "summary": {"ok": 1, "warn": 1, "fail": 1}
}

@pytest.fixture(autouse=True)
def setup_quality_report(tmp_path, monkeypatch):
    # Crea .evidence/iac-quality-report.json temporal
    evidence_dir = tmp_path / ".evidence"
    evidence_dir.mkdir()
    report_path = evidence_dir / "iac-quality-report.json"
    with open(report_path, "w") as f:
        json.dump(QUALITY_REPORT, f)
    # Crea data/modules_index.json temporal
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    modules_index = [
        {
            "id": "mod-001",
            "name": "example-az",  
            "type": "terraform",
            "path": "modules/terraform/example-az", 
            "version": "1.0.0",
            "tags": ["azure", "example"],
            "quality_state": "OK"
        },
        {
            "id": "mod-002",
            "name": "example-nginx",
            "type": "k8s",
            "path": "modules/k8s/example-nginx",
            "version": "0.1.0",
            "tags": ["k8s", "nginx"],
            "quality_state": "WARN"
        },
        {
            "id": "mod-003",
            "name": "local-docker",
            "type": "terraform",
            "path": "modules/terraform/local-docker",
            "version": "1.0.0",
            "tags": ["docker", "local"],
            "quality_state": "FAIL"
        },
        {
            "id": "mod-004",
            "name": "example-local-",
            "type": "terraform",
            "path": "modules/terraform/example-local",
            "version": "1.0.0",
            "tags": ["local", "filesystem"],
            "quality_state": "OK"
        }
    ]
    with open(data_dir / "modules_index.json", "w") as f:
        json.dump(modules_index, f)
    # Monkeypatch cwd para que la app lo encuentre
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield
    os.chdir(old_cwd)

client = TestClient(app)

def test_module_quality_state():
    resp = client.get("/modules/mod-001")
    assert resp.status_code == 200
    assert resp.json()["quality_state"] == "OK"

    resp = client.get("/modules/mod-003")
    assert resp.status_code == 200
    assert resp.json()["quality_state"] == "FAIL"

def test_filter_by_quality_state():
    resp = client.get("/modules?filter=quality_state:OK")
    assert resp.status_code == 200
    ids = [m["id"] for m in resp.json()]
    assert "mod-001" in ids
    assert "mod-003" not in ids

    resp = client.get("/modules?filter=quality_state:FAIL|WARN")
    assert resp.status_code == 200
    ids = [m["id"] for m in resp.json()]
    assert set(ids) & {"mod-002", "mod-003"} == {"mod-002", "mod-003"}
