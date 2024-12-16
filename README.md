# Web-приложение для определения заполненных форм

## Описание проекта

Это веб-приложение реализует API для работы с шаблонами форм. Оно позволяет:
1. Добавлять новые шаблоны форм в базу данных.
2. Искать подходящий шаблон формы на основе входных данных.
3. Автоматически определять типы полей, если шаблон не найден.

Поддерживаются следующие типы данных:
- **email**: Адрес электронной почты.
- **phone**: Телефон в формате `+7 XXX XXX XX XX`.
- **date**: Дата в формате `YYYY-MM-DD` или `DD.MM.YYYY`.
- **text**: Текстовые данные без особых требований.

---

## Технологии

- **Язык программирования**: Python 3.6+
- **Фреймворк**: Flask
- **База данных**: TinyDB (встроенная NoSQL база данных)
- **HTTP-клиент**: Requests (для тестирования API)

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <URL_вашего_репозитория>
cd <название_проекта>
```

### 2. Установка зависимостей

Убедитесь, что у вас установлен Python версии 3.6 или выше. Установите зависимости с помощью команды:

```bash
pip install -r requirements.txt
```

### 3. Запуск приложения

Для запуска веб-приложения выполните команду:

```bash
python app.py
```

После этого приложение будет доступно по адресу: [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Использование API

### 1. Добавление шаблона формы

- **URL**: `/add_template`
- **Метод**: POST
- **Тело запроса** (в формате JSON):
  ```json
  {
    "name": "Form Name",
    "field_name_1": "email",
    "field_name_2": "phone"
  }
  ```
- **Пример запроса**:
  ```bash
  curl -X POST http://127.0.0.1:5000/add_template \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Form", "user_email": "email", "user_phone": "phone"}'
  ```
- **Ответ при успешном добавлении**:
  ```json
  {
    "message": "Template added successfully!"
  }
  ```
- **Ответ при ошибке**:
  ```json
  {
    "error": "Template with this name already exists"
  }
  ```

### 2. Поиск подходящей формы

- **URL**: `/get_form`
- **Метод**: POST
- **Тело запроса** (в формате form-data):
  ```
  field_name_1=value1&field_name_2=value2
  ```
- **Пример запроса**:
  ```bash
  curl -X POST http://127.0.0.1:5000/get_form \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_email=test@example.com&user_phone=+7 123 456 78 90"
  ```
- **Ответ при успешном поиске шаблона**:
  ```json
  {
    "template_name": "Test Form"
  }
  ```
- **Ответ, если шаблон не найден**:
  ```json
  {
    "field_name_1": "email",
    "field_name_2": "text"
  }
  ```

---

## Тестирование

### 1. Запуск тестов

Убедитесь, что приложение запущено. Выполните тесты с помощью команды:

```bash
python test_requests.py
```

### 2. Примеры тестовых ответов

- **Добавление шаблона**:
  ```
  Add Template Response: {'message': 'Template added successfully!'}
  ```
- **Поиск подходящей формы**:
  ```
  Get Form Response: {'template_name': 'Test Form'}
  ```
- **Типизация полей при отсутствии совпадений**:
  ```
  No Match Response: {'random_field': 'text', 'unknown_field': 'text'}
  ```

---

## Структура проекта

```
.
├── app.py                 # Основной файл приложения
├── forms_db.json          # База данных TinyDB
├── requirements.txt       # Зависимости проекта
├── test_requests.py       # Скрипт для тестирования API
├── README.md              # Документация проекта
```

---

## Docker (опционально)

### 1. Создание Dockerfile

Создайте файл `Dockerfile` в корне проекта:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### 2. Сборка Docker-образа

Соберите Docker-образ с помощью команды:

```bash
docker build -t forms-app .
```

### 3. Запуск контейнера

Запустите контейнер:

```bash
docker run -p 5000:5000 forms-app
```

После этого приложение будет доступно по адресу: [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Примеры использования

### Пример добавления нового шаблона

```bash
curl -X POST http://127.0.0.1:5000/add_template \
-H "Content-Type: application/json" \
-d '{"name": "Registration Form", "email_field": "email", "phone_field": "phone"}'
```

### Пример поиска формы

```bash
curl -X POST http://127.0.0.1:5000/get_form \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "email_field=test@example.com&phone_field=+7 999 123 45 67"
```

---

## Зависимости

Для работы приложения необходимы следующие библиотеки:
- Flask
- TinyDB
- Requests (для тестирования)

### Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## Примечания

- Для удобства рекомендуется использовать Python версии 3.6 и выше.
- TinyDB используется как простая встраиваемая база данных. При желании можно заменить TinyDB на MongoDB для более сложных сценариев.

---

## Контакты

Если у вас есть вопросы или предложения, напишите мне:

- **Email**: <azi-han@mail.ru>

Спасибо за использование! 🚀