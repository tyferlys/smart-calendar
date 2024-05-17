import asyncio
from fastapi.testclient import TestClient
from loguru import logger

from src.api.main import app

headers = {
    'x-token': 'hn85623478Fgr8372gjm87kKDHF'
}


async def test_get_client():
    telegram_id = "1"

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.get(f"/{telegram_id}")
    data = response.json()

    assert response.status_code == 200 and data["phone"] == "79873572114"
    logger.success("ТЕСТ НА ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ УСПЕШНО ВЫПОЛНЕН")

    response = client.get(f"/2")
    data = response.json()

    assert data == None
    logger.success("ТЕСТ НА ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ УСПЕШНО ВЫПОЛНЕН")


async def test_get_clients():
    params = {
        "page": 1,
        "count": 1
    }

    params2 = {
        "page": 1,
        "count": 2
    }

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.get("/", params=params2)
    data = response.json()

    assert response.status_code == 200 and len(data["clients"]) == 2
    logger.success("ТЕСТ НА ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЕЙ УСПЕШНО ВЫПОЛНЕН")


async def test_create_client():
    payload = {
        "last_name": "Асмолов",
        "first_name": "Антон",
        "middle_name": "Борисович",
        "phone": "79873572113",
        "username": "kio",
        "telegram_id": "1234"
    }

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.post("", json=payload)
    data = response.json()

    assert response.status_code == 201 and data["telegram_id"] == "1234"
    logger.success("ТЕСТ НА СОЗДАНИЯ КЛИЕНТА УСПЕШНО ВЫПОЛНЕН")


async def test_create_client_with_error():
    payload = {
        "last_name": "Асмолов",
        "first_name": "Антон",
        "middle_name": "Борисович",
        "phone": "79873572113",
        "username": "kio",
        "telegram_id": "1234"
    }

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.post("", json=payload)
    data = response.json()

    assert response.status_code == 500
    logger.success("ТЕСТ НА СОЗДАНИЯ КЛИЕНТА УСПЕШНО ВЫПОЛНЕН")


async def test_put_client():
    payload = {
        "id": 7,
        "last_name": "Асмолов",
        "first_name": "Антон",
        "middle_name": "Аскарович",
        "phone": "79873572113",
        "username": "kio",
        "telegram_id": "1234"
    }

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.put("", json=payload)
    data = response.json()

    assert response.status_code == 200 and data["middle_name"] == "Аскарович"
    logger.success("ТЕСТ НА обновление КЛИЕНТА УСПЕШНО ВЫПОЛНЕН")


async def test_put_client_with_error():
    payload = {
        "id": 8,
        "last_name": "Асмолов",
        "first_name": "Антон",
        "middle_name": "Аскарович",
        "phone": "79873572113122",
        "username": "kioss",
        "telegram_id": "12345"
    }

    client = TestClient(app, base_url=f'http://testserver/clients', headers=headers)
    response = client.put("", json=payload)
    data = response.json()

    assert response.status_code == 500
    logger.success("ТЕСТ НА обновление КЛИЕНТА УСПЕШНО ВЫПОЛНЕН")


if __name__ == '__main__':
    asyncio.run(test_put_client_with_error())