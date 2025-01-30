from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_qr():
    url = "https://example.com"  # Use a valid URL here
    response = client.post("/generate-qr/", json={"url": url})
    
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check that the response contains the 'qr_code_url' field
    assert "qr_code_url" in response.json()

def test_generate_qr_invalid_url():
    url = "invalid-url"  # Invalid URL
    response = client.post("/generate-qr/", json={"url": url})

    # FastAPI validation should return status 422 for invalid input
    assert response.status_code == 422  
