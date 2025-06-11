from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    operation = None
    numbers = []
    
    if request.method == 'POST':
        input_method = request.form.get('input_method', 'single')
        
        if input_method == 'single':
            numbers_str = request.form.get('numbers', '')
            try:
                numbers = [float(num) for num in numbers_str.split()]
                if len(numbers) != 3:
                    raise ValueError("Нужно ввести ровно 3 числа")
            except ValueError as e:
                return render_template('index.html', error=str(e))
        else:
            try:
                num1 = float(request.form.get('num1', 0))
                num2 = float(request.form.get('num2', 0))
                num3 = float(request.form.get('num3', 0))
                numbers = [num1, num2, num3]
            except ValueError:
                return render_template('index.html', error="Пожалуйста, введите корректные числа")
        
        operation = request.form.get('operation')
        
        if operation == 'min':
            result = min(numbers)
        elif operation == 'max':
            result = max(numbers)
        elif operation == 'avg':
            result = sum(numbers) / len(numbers)
    
    return render_template('index.html', 
                         result=result, 
                         operation=operation,
                         numbers=numbers)

if __name__ == '__main__':
    app.run(debug=True)