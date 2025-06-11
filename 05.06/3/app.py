from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'age': request.form.get('age'),
            'email': request.form.get('email'),
            'gender': request.form.get('gender'),
            'address': request.form.get('address'),
            'subscribe': 'Да' if request.form.get('subscribe') else 'Нет'
        }
        return render_template('result.html', user_data=user_data)
    
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)