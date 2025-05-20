from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        favorite_language = request.form.get('language')
        return render_template('thankyou.html', language=favorite_language)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)