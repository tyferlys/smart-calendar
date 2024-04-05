import asyncio
from fastapi.testclient import TestClient

from src.api.main import app

headers = {
    'x-token': 'hn85623478Fgr8372gjm87kKDHF'
}


async def test_get_option_client():
    client = TestClient(app, base_url='http://testserver/options_clients', headers=headers)
    response = client.get("943091362")
    assert response.status_code == 200


async def test_put_option_client():
    client = TestClient(app, base_url='http://testserver/options_clients', headers=headers)
    payload = {"id": "5", "id_client": "6", "is_notification": False, "timezone": 0}
    response = client.put("/", json=payload)
    assert response.status_code == 200


if __name__ == '__main__':
    # asyncio.run(test_get_option_client())
    asyncio.run(test_put_option_client())
