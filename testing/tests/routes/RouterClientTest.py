import asyncio
from fastapi.testclient import TestClient

from src.api.main import app

headers = {
    'x-token': 'hn85623478Fgr8372gjm87kKDHF'
}


async def test_get_client():
    telegram_id = "380903828"

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.get(f"/{telegram_id}")
    data = response.json()

    assert response.status_code == 200 and data["phone"] == "79873572114"


async def test_get_clients():
    params = {
        "page": 1,
        "count": 2
    }

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.get("/", params=params)
    data = response.json()

    assert response.status_code == 200 and len(data["clients"]) == 2


if __name__ == '__main__':
    asyncio.run(test_get_clients())