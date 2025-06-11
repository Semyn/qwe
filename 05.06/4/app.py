from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

def calculate_programmer_day(year):
    try:
        year = int(year)
        date = datetime(year, 1, 1) + timedelta(days=255)
        return date.strftime("%d %B (%A)")
    except ValueError:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    year = None
    
    if request.method == 'POST':
        year = request.form.get('year')
        result = calculate_programmer_day(year)
    
    return render_template('index.html', result=result, year=year)

if __name__ == '__main__':
    app.run(debug=True)