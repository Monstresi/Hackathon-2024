from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    print(f"User entered: {user_input}")
    
    # Render the HTML with the server response
    return render_template('index.html', message=f'You entered: {user_input}')

if __name__ == '__main__':
    app.run(debug=True)
