import asyncio
import json

from fastapi.testclient import TestClient
from loguru import logger

from src.api.main import app

headers = {
    'x-token': 'hn85623478Fgr8372gjm87kKDHF'
}


def test_get_option_client():
    # валидное получение настреок юзера
    client = TestClient(app, base_url='http://testserver/options_clients', headers=headers)
    response = client.get("123451234")
    asserted_response = {'id': 1, 'id_client': 2, 'is_notification': False, 'timezone': 0}
    assert response.status_code == 200
    assert json.loads(response.text) == asserted_response
    logger.success("ТЕСТ НА ВАЛИДНОЕ ПОЛУЧЕНИЕ НАСТРОЕК УСПЕШНО ВЫПОЛНЕН")

    # не найдены настроки
    response = client.get('1')
    assert response.status_code == 500
    logger.success("ТЕСТ НА ОШИБКУ ПРИ ПОЛУЧЕНИИ НАСТРОЕК УСПЕШНО ВЫПОЛНЕН")


def test_put_option_client():
    # валидный кейс изменения настроек
    client = TestClient(app, base_url='http://testserver/options_clients', headers=headers)
    payload = {"id": 1, "id_client": 2, "is_notification": False, "timezone": 0}
    response = client.put("/", json=payload)
    result = {"id": 1, "id_client": 2, "is_notification": False, "timezone": 0}
    assert response.status_code == 200
    assert result == json.loads(response.text)
    logger.success("ТЕСТ НА ВАЛИДНОЕ ИЗМЕНЕНИЕ НАСТРОЕК УСПЕШНО ВЫПОЛНЕН")

    # клиент не найден
    payload = {"id": 1, "id_client": 4, "is_notification": False, "timezone": 0}
    response = client.put("/", json=payload)
    assert response.status_code == 500
    logger.success("ТЕСТ НА ОШИБКУ ПРИ ОБНОВЛЕНИИ НАСТРОЕК ( КЛИЕНТ НЕ НАЙДЕН ) УСПЕШНО ВЫПОЛНЕН")

    # настройки не найдены
    payload = {"id": 3, "id_client": 1, "is_notification": False, "timezone": 0}
    response = client.put("/", json=payload)
    assert response.status_code == 500
    logger.success("ТЕСТ НА ОШИБКУ ПРИ ОБНОВЛЕНИ НАСТРОЕК ( НАСТРОЙКИ НЕ НАЙДЕНЫ ) УСПЕШНО ВЫПОЛНЕН")


def main():
    # test_get_option_client()
    test_put_option_client()


if __name__ == '__main__':
    main()
