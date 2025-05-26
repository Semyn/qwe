
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def form():
    data = {
        'name': request.args.get('name', ''),
        'surname': request.args.get('surname', ''),
        'email': request.args.get('email', ''),
        'age': request.args.get('age', ''),
        'gender': request.args.get('gender', ''),
        'hobbies': request.args.getlist('hobbies'),
        'city': request.args.get('city', '')
    }
    return render_template('form.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)