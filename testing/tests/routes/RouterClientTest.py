import asyncio
from fastapi.testclient import TestClient
from loguru import logger

from src.api.main import app

headers = {
    'x-token': 'hn85623478Fgr8372gjm87kKDHF'
}


async def test_get_client():
    telegram_id = "943091362"

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.get(f"/{telegram_id}")
    data = response.json()

    assert response.status_code == 200 and data["phone"] == "78888888888"
    logger.success("ТЕСТ НА ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ УСПЕШНО ВЫПОЛНЕН")


async def test_get_clients():
    params = {
        "page": 1,
        "count": 2
    }

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.get("/", params=params)
    data = response.json()
    print(data)
    # assert response.status_code == 200 and len(data["clients"]) == 2


if __name__ == '__main__':
    asyncio.run(test_get_client())