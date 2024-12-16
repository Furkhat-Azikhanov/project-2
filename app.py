from flask import Flask, request, jsonify  # Импорт Flask для создания веб-приложения
from tinydb import TinyDB, Query  # Импорт TinyDB для работы с базой данных
import re  # Импорт модуля регулярных выражений для валидации
import logging  # Импорт модуля логирования
import traceback  # Импорт модуля для обработки ошибок
import os  # Импорт модуля для работы с файловой системой

# Инициализация Flask приложения
app = Flask(__name__)

# Проверяем, существует ли файл базы данных, если нет, создаем его
if not os.path.exists('forms_db.json'):
    with open('forms_db.json', 'w') as f:
        f.write('{}')  # Создаем пустую базу данных

# Инициализация базы данных TinyDB
db = TinyDB('forms_db.json')  # Открываем или создаем файл базы данных
forms_table = db.table('forms')  # Создаем или получаем таблицу "forms" из базы

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Устанавливаем уровень логирования на INFO
logger = logging.getLogger(__name__)  # Создаем объект логгера

# Начальные данные для таблицы (шаблоны форм)
default_forms = [
    {
        "name": "User Registration",  # Название шаблона
        "user_email": "email",  # Поле с типом email
        "user_phone": "phone"  # Поле с типом phone
    },
    {
        "name": "Order Form",  # Название шаблона
        "order_date": "date",  # Поле с типом date
        "customer_email": "email"  # Поле с типом email
    }
]

# Заполняем таблицу, если она пуста
try:
    if not forms_table.all():  # Проверяем, есть ли данные в таблице
        forms_table.insert_multiple(default_forms)  # Добавляем начальные шаблоны
        logger.info("Default forms added to the database.")  # Логируем успешное добавление
except Exception as e:
    logger.error(f"Error initializing database: {e}")  # Логируем ошибки при инициализации

# Функция для валидации типа поля
def validate_field(value):
    # Проверяем, является ли поле телефоном
    if re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", value):
        return "phone"
    # Проверяем, является ли поле датой (в формате YYYY-MM-DD или DD.MM.YYYY)
    elif re.match(r"^\d{4}-\d{2}-\d{2}$|^\d{2}\.\d{2}\.\d{4}$", value):
        return "date"
    # Проверяем, является ли поле email-адресом
    elif re.match(r"^[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}$", value):
        return "email"
    # Если поле не соответствует другим типам, возвращаем "text"
    else:
        return "text"

# Эндпоинт для добавления шаблона формы
@app.route('/add_template', methods=['POST'])
def add_template():
    try:
        logger.info(f"Received data: {request.json}")  # Логируем полученные данные
        template_data = request.json  # Извлекаем JSON из запроса
        # Проверяем, что переданы корректные данные
        if not template_data or "name" not in template_data or len(template_data) < 2:
            logger.error("Invalid template format received")  # Логируем ошибку формата
            return jsonify({"error": "Invalid template format"}), 400

        # Проверяем, существует ли уже шаблон с таким именем
        existing_template = forms_table.search(Query().name == template_data["name"])
        if existing_template:
            logger.error(f"Template with name '{template_data['name']}' already exists")  # Логируем ошибку
            return jsonify({"error": "Template with this name already exists"}), 400

        forms_table.insert(template_data)  # Добавляем новый шаблон в базу данных
        logger.info(f"Template added: {template_data}")  # Логируем успешное добавление
        return jsonify({"message": "Template added successfully!"})  # Возвращаем успешный ответ
    except Exception as e:
        logger.error(f"Error in add_template: {e}")  # Логируем ошибку
        logger.error(traceback.format_exc())  # Логируем стек ошибки
        return jsonify({"error": "An unexpected error occurred"}), 500  # Возвращаем ошибку

# Эндпоинт для поиска подходящей формы
@app.route('/get_form', methods=['POST'])
def get_form():
    try:
        logger.info(f"Received data: {request.form.to_dict()}")  # Логируем входные данные
        input_data = request.form.to_dict()  # Получаем данные из POST-запроса
        if not input_data:  # Проверяем, что данные не пусты
            logger.error("No data provided in request")  # Логируем ошибку
            return jsonify({"error": "No data provided"}), 400

        # Перебираем все шаблоны в базе данных
        for template in forms_table.all():
            logger.info(f"Checking template: {template}")  # Логируем текущий шаблон
            template_name = template.get("name")  # Извлекаем название шаблона
            if not template_name:  # Пропускаем, если название отсутствует
                continue

            template_copy = template.copy()  # Копируем шаблон
            template_copy.pop("name", None)  # Удаляем поле "name" из проверки

            # Проверяем, совпадают ли поля шаблона с переданными данными
            if all(
                key in input_data and validate_field(input_data[key]) == value
                for key, value in template_copy.items()
            ):
                logger.info(f"Matching template found: {template_name}")  # Логируем найденный шаблон
                return jsonify({"template_name": template_name})  # Возвращаем название шаблона

        # Если шаблон не найден, типизируем поля на лету
        logger.info("No matching template found. Returning field types.")  # Логируем отсутствие совпадений
        response = {key: validate_field(value) for key, value in input_data.items()}  # Типизация полей
        return jsonify(response)  # Возвращаем типы полей
    except Exception as e:
        logger.error(f"Error in get_form: {e}")  # Логируем ошибку
        logger.error(traceback.format_exc())  # Логируем стек ошибки
        return jsonify({"error": "An unexpected error occurred"}), 500  # Возвращаем ошибку

# Точка входа
if __name__ == '__main__':
    try:
        logger.info(f"Loaded forms: {forms_table.all()}")  # Логируем загруженные шаблоны
    except Exception as e:
        logger.error(f"Error loading forms: {e}")  # Логируем ошибку загрузки базы данных
    app.run(debug=True)  # Запускаем приложение в режиме отладки
