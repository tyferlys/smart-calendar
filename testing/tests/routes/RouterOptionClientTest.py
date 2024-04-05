import asyncio
import json

from fastapi.testclient import TestClient

from src.api.main import app

headers = {
    'x-token': 'hn85623478Fgr8372gjm87kKDHF'
}


async def test_get_option_client():
    # валидное получение настреок юзера
    client = TestClient(app, base_url='http://testserver/options_clients', headers=headers)
    response = client.get("943091362")
    assert response.status_code == 200

    # не найдены настроки
    response = client.get('12312321')
    assert response.status_code == 500
    assert response.text == '"ошибка при поиске"'


async def test_put_option_client():
    # валидный кейс изменения настроек
    client = TestClient(app, base_url='http://testserver/options_clients', headers=headers)
    payload = {"id": "5", "id_client": "6", "is_notification": False, "timezone": 0}
    response = client.put("/", json=payload)
    result = {"id": 5, "id_client": 6, "is_notification": False, "timezone": 0}
    assert response.status_code == 200
    assert result == json.loads(response.text)

    # клиент не найден
    payload = {"id": 6, "id_client": 4, "is_notification": False, "timezone": 0}
    response = client.put("/", json=payload)
    assert response.text == '"ошибка при поиске"'
    assert response.status_code == 500

    # настройки не найдены
    payload = {"id": 6, "id_client": 6, "is_notification": False, "timezone": 0}
    response = client.put("/", json=payload)
    assert response.text == '"ошибка при поиске"'
    assert response.status_code == 500


if __name__ == '__main__':
    # asyncio.run(test_get_option_client())
    asyncio.run(test_put_option_client())
