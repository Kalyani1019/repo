# import sys
# import os

# # Add the parent directory of the test folder to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from main import app  # Now this should work!
# from fastapi.testclient import TestClient

# client = TestClient(app)

# def test_shorten_url():
#     response = client.post("/shorten", json={"long_url": "https://www.example.com/blog/devops/best-tools-for-infrastructure-automation-in-2025?source=guide&utm_campaign=devops&utm_medium=article&utm_source=chatgpt"})
#     assert response.status_code == 200
#     assert "short_url" in response.json()

import sys
import os

# Add the parent directory of the test folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # Import FastAPI app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_shorten_url():
    url_to_shorten = input("Enter a URL to shorten: ")  # Take user input
    response = client.post("/shorten/", json={"url": url_to_shorten})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "short_url" in data
    print(f"Shortened URL: {data['short_url']}")
