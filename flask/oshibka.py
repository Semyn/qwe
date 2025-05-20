from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get("name")
    return f"hello {name}"

if __name__ == "__main__":
    app.run(debug=True)