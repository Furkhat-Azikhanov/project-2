import requests  # Импортируем библиотеку requests для выполнения HTTP-запросов

# Базовый URL для тестирования API
BASE_URL = "http://127.0.0.1:5000"

# Функция для обработки JSON-ответов
def safe_json_response(response):
    print(f"Response Status Code: {response.status_code}")  # Печатаем статус ответа
    print(f"Response Text: {response.text}")  # Печатаем текст ответа
    try:
        # Пытаемся декодировать JSON-ответ
        return response.json()
    except requests.exceptions.JSONDecodeError:
        # Возвращаем ошибку, если JSON-декодирование не удалось
        return {"error": f"Failed to decode JSON. Status code: {respons