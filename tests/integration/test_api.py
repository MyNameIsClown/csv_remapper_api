import os
import pytest
import shutil
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_files():
    # Ensure a clean files directory before and after tests
    if os.path.isdir("files"):
        shutil.rmtree("files")
    yield
    if os.path.isdir("files"):
        shutil.rmtree("files")


def upload_sample(tmp_path, content):
    sample = tmp_path / "sample.csv"
    sample.write_text(content)
    files = {"file": ("sample.csv", open(sample, "rb"))}
    response = client.post("/api/v1/csv-file/", files=files)
    assert response.status_code == 200
    return response.json()["file_id"]


def test_create_and_rename_key(tmp_path):
    # Test full flow: upload and rename header
    csv_content = "col1,col2\n1,2\n3,4\n"
    file_id = upload_sample(tmp_path, csv_content)
    # Rename col1 to new1
    resp = client.put(
        f"/api/v1/csv-file/{file_id}/rename-key/", json={"key_names": ["col1", "new1"]}
    )
    assert resp.status_code == 200
    # Verify file content updated
    with open(f"files/{file_id}.csv") as f:
        first_line = f.readline().strip()
    assert first_line == "new1,col2"


def test_missing_file_error(tmp_path):
    # Try operations on nonexistent ID
    fake_id = "00000000-0000-4000-8000-000000000000"
    resp = client.put(
        f"/api/v1/csv-file/{fake_id}/remove-key", json={"key_name": "any"}
    )
    assert resp.status_code == 400


def test_multiple_operations(tmp_path):
    # Upload and test rename-keys, remove-keys, normalize, and merge
    csv_content = "a,b,date\n-1,2,2020-01-01\n-3,4,2020-02-02\n"
    file_id = upload_sample(tmp_path, csv_content)
    # Rename keys
    resp = client.put(
        f"/api/v1/csv-file/{file_id}/rename-keys/", 
        json={"key_dict": {"a": "A", "b": "B", "date": "Date"}}
    )
    assert resp.status_code == 200
    # Normalize to positive
    resp = client.put(
        f"/api/v1/csv-file/{file_id}/normalize-values", 
        json={"key": "A", "mode": "to_positive"}
    )
    assert resp.status_code == 200
    # Merge keys A and B into AB
    resp = client.put(
        f"/api/v1/csv-file/{file_id}/merge-keys", 
        json={
            "ordered_keys": ["A", "B"],
            "connector": {"type": 1, "operator": "+"},
            "new_key_name": "AB"
        }
    )
    assert resp.status_code == 200
    assert resp.json() == "Merge complete"
    # Final file should exist
    assert os.path.isfile(f"files/{file_id}.csv")