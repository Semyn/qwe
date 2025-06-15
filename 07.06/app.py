from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        if not name or not email:
            flash('Пожалуйста, заполните все поля', 'danger')
        else:
            flash(f'Спасибо, {name}! Ваш email: {email}', 'success')
            return redirect(url_for('index'))
    
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)