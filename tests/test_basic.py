from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_main():
    test_file = 'test_file.docx'
    file = {'file': ('test_file.docx', open(test_file, 'rb'))}
    response = client.post(
        url="/api/v1/csv-file",
        files=file
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}