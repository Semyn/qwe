# 1. Работа с формами (Flask-WTF)
Текстовый ответ:
Для создания формы регистрации в Flask используется расширение Flask-WTF. Форма должна включать поля для имени пользователя, email, пароля и подтверждения пароля. Добавляются валидаторы: обязательность полей, проверка email, совпадение паролей. В шаблоне форма отображается с возможностью показа ошибок валидации под каждым полем. После отправки данные проверяются и сохраняются в БД.

Пример кода:

# forms.py
    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField, SubmitField
    from wtforms.validators import DataRequired, Email, EqualTo

    class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Register')

# routes.py
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)
# 2. Авторизация пользователей (Flask-Login)
Текстовый ответ:
Для работы с Flask-Login класс User должен наследовать UserMixin и реализовать методы is_authenticated, is_active и др. Страница входа проверяет учетные данные, а кнопка выхода завершает сессию. Защита страниц осуществляется декоратором @login_required.

Пример кода:

# models.py
    from flask_login import UserMixin

    class User(UserMixin, db.Model):

    
        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

# routes.py
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
# 3. Хранение данных пользователя (Flask Session)
Текстовый ответ:
Flask-Login автоматически сохраняет ID пользователя в сессии при входе. Проверить авторизацию можно через current_user.is_authenticated. Для выхода используется logout_user(), который очищает сессию.

Пример кода:

# Проверка авторизации
    if current_user.is_authenticated:
        print("User is logged in")

# Выход
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
# 4. Работа с базой данных (Flask-SQLAlchemy)
Текстовый ответ:
Модель Post создается с полями id, title, content, date_posted и user_id (внешний ключ). Таблицы создаются при первом запуске через db.create_all(). CRUD операции выполняются через SQLAlchemy ORM.

Пример кода:

# models.py
    class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100))
        content = db.Column(db.Text)
        date_posted = db.Column(db.DateTime, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Создание записи
    post = Post(title='First Post', content='Content', author=current_user)
    db.session.add(post)
    db.session.commit()
# 5. Всплывающие сообщения (Flask Flash)
Текстовый ответ:
Сообщения создаются через flash() с указанием категории. В шаблоне выводятся через get_flashed_messages(). Они показываются один раз, так как удаляются из сессии после отображения.

Пример кода:

# Отправка сообщения
    flash('Profile updated successfully!', 'success')

# Шаблон
    {% for category, message in get_flashed_messages(with_categories=true) %}
    <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
# 6. Основы Flask
Текстовый ответ:
Главная страница и профиль создаются как обычные маршруты. Общий дизайн реализуется через базовый шаблон (base.html) с блоками для контента, который расширяется дочерними шаблонами.

Пример кода:

# routes.py
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/user/<username>')
    def profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('profile.html', user=user)

# base.html
    <html>
    <head>{% block head %}{% endblock %}</head>
    <body>
        {% include 'navbar.html' %}
        {% block content %}{% endblock %}
    </body>
    </html>

# home.html
    {% extends "base.html" %}
    {% block content %}
    <h1>Welcome!</h1>
    {% endblock %}