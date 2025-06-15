from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

class FeedbackForm(FlaskForm):
    name = StringField('Имя', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(min=2, max=100, message="Имя должно быть от 2 до 100 символов")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Email(message="Введите корректный email адрес"),
        Length(max=100)
    ])
    message = TextAreaField('Сообщение', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(min=10, message="Сообщение должно быть не менее 10 символов")
    ])
    submit = SubmitField('Отправить')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Ваше сообщение успешно отправлено!', 'success')
        return redirect(url_for('index'))
    return render_template('feedback.html', form=form)

@app.route('/submissions')
def submissions():
    all_feedback = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template('submissions.html', feedbacks=all_feedback)

if __name__ == '__main__':
    app.run(debug=True)