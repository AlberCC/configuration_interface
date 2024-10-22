##################################################
# File: app.py
# Author: Alberto Caldas Camacho
##################################################
from flask import Flask, render_template, request
import json
import configparser

# Initialize the Flask app
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/form')
def form():
    try:
        with open('./static/template-json/template.json') as f:
            template_json = json.load(f)
            variables = template_json.get('Variables')
            if variables is None:
                return "Variables not found. Be aware of the spelling of the Variables object.", 404
            types = template_json.get('Types')
            if types is None:
                return "Types not found. Be aware of the spelling of the Types object.", 404
            enums = template_json.get('Enums')
            if enums is None:
                return "Enums not found. Be aware of the spelling of the Enums object.", 404
    except FileNotFoundError:
        return "JSON file not found", 404
    except json.JSONDecodeError:
        return "Error decoding JSON", 400
    return render_template('form.html', variables=variables, types=types, enums=enums)

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    ini_data = generate_ini(form_data)
    
    ini_filename = './files/config.ini'

    with open(ini_filename, 'w') as configfile:
        # Escribir manualmente las líneas en blanco
        flag = False
        for section in ini_data.sections():
            if flag:
                configfile.write('\n\n\n')

            configfile.write(f'\n[{section}]')
            flag = True
            previous_i = '0'

            for key, value in ini_data.items(section):
                if '[' not in key:
                    configfile.write(f'\n{key} = {value}')
                
                else: # Si la clave contiene corchetes, es una clave compuesta
                    i = key.split('[')[1].split(']')[0]
                    if previous_i == i:
                        configfile.write(f'\n{key} = {value}')

                    else: # Si el índice cambió, añadir una línea en blanco
                        previous_i = i
                        configfile.write('\n')
                        configfile.write(f'\n{key} = {value}')

            
        
    return f"Archivo INI generado: <a href='/{ini_filename}'>{ini_filename}</a>"

#Función para generar el archivo ini
def generate_ini(form_data):
    
    config = configparser.ConfigParser() 

    for key, value in form_data.items():
        if ']' in key:
            section, option = key.split('[')
            if section not in config:
                config[section] = {}
            config[section][key] = value

        elif '.' in key:
            section, option = key.split('.')
            if section not in config:
                config[section] = {}
            config[section][key] = value

        else:
            config['DEFAULT'][key] = value
    
    return config

# Execute the app
if __name__ == '__main__':
    app.run(debug=True)