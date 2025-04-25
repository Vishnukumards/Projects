from flask import Flask,render_template,request

app = Flask(__name__)


class Simple_Calculator:
    @staticmethod
    def Addition(value1,value2):
        return value1+value2
    
    @staticmethod
    def Subtraction(value1,value2):
        return value1-value2
    
    @staticmethod
    def multiplication(value1,value2):
        return value1*value2
    
    @staticmethod
    def division(value1,value2):
        if value2 == 0:
            return "Division by zero is undefined"
        return value1/value2
    
    @staticmethod
    def percentage(value1,value2):
        if value2 == 0:
            return "Cannot calculate percentage with divisor zero"
        return (value1/value2)*100
    
@app.route('/',methods= ['GET', 'POST'])
def calculator():
    result = None
    if request.method =='POST':
        value1 = float(request.form.get('value1',0))
        value2 = float(request.form.get('value2',0))
        
        operation = request.form.get('operation')
        
        calculator = Simple_Calculator()
        
        if operation == 'add':
            result = calculator.Addition(value1,value2)
            
        elif operation == 'subtract':
            result = calculator.Subtraction(value1,value2)
            
        elif operation == 'multiply':
            result = calculator.multiplication(value1,value2)
            
        elif operation == 'divide':
            result = calculator.division(value1,value2)
            
        elif operation == 'percentage':
            result = calculator.percentage(value1,value2)
            
            
    return render_template('index.html',result =result)
    
if __name__ == '__main__':
    app.run(debug=True)