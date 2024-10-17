##################################################
# File: app.py
# Author: Alberto Caldas Camacho
##################################################
from flask import Flask, render_template
import json

# Initialize the Flask app
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    with open('./static/json/template.json') as f:
        template_json = json.load(f)
        variables, types= template_json['Variables'], template_json['Types'] ##Añadir los try catch o como sea en python
    return render_template('form.html', variables=variables, types=types)


# Execute the app
if __name__ == '__main__':
    app.run(debug=True)