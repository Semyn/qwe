Стандартная структура проекта:

    text
    flask_app/
    ├── app.py                  # Основной файл приложения
    |
    ├── static/                 # Статические файлы
    │   ├── css/
    │   ├── js/
    │   └── images/
    ├── templates/              
    │   ├── base.html           # Базовый шаблон
    │   ├── index.html          # Главная страница




3. Основные механизмы Flask
Маршрутизация (@app.route)
python
from flask import Flask
app = Flask(__name__)

# Обработка GET-запроса
@app.route('/')
def home():
    return 'Главная страница'

# Обработка с переменной в URL
@app.route('/user/<username>')
def show_user(username):
    return f'Пользователь: {username}'

# Обработка нескольких методов
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Обработка данных формы
        pass
    # Показ формы для GET-запроса
    return render_template('login.html')
Обработка запросов
python
from flask import request

@app.route('/submit', methods=['POST'])
def submit():
    # Получение данных формы
    name = request.form.get('name')
    email = request.form.get('email')
    
    # Получение параметров GET-запроса
    search_query = request.args.get('q')
    
    # Получение JSON данных
    if request.is_json:
        data = request.get_json()
Шаблоны Jinja2
Пример base.html:


    ```<!DOCTYPE html>
    <html>
    <head>
        <title>{% block title %}{% endblock %}</title>
    </head>
    <body>
        {% block content %}{% endblock %}
    </body>
    </html>```
Пример index.html:


    ```{% extends "base.html" %}

    {% block title %}Главная{% endblock %}

    {% block content %}
        <h1>Добро пожаловать</h1>
        {% if current_user.is_authenticated %}
            <p>Вы вошли как {{ current_user.username }}</p>
        {% else %}
            <a href="{{ url_for('login') }}">Войти</a>
        {% endif %}
    {% endblock %}```
Работа с формами
С Flask-WTF:


    ```from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField
    from wtforms.validators import DataRequired

    class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])```
Обработка формы:


    ```@app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # Проверка учетных данных
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
        return render_template('login.html', form=form)```
Подключение к базе данных
С Flask-SQLAlchemy:


    ```from flask_sqlalchemy import SQLAlchemy

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', users=users)```

