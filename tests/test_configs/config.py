from fastapi.testclient import TestClient
from BlogFastAPI.app.main import app

client = TestClient(app)