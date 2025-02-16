import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import json
import time

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Validar que todas las variables necesarias estén presentes en las variables de entorno
required_env_vars = ['SINRIC_API_KEY', 'SINRIC_DEVICE_ID', 'SINRIC_PORTAL_ID', 'SINRIC_TOKEN_ID']
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Falta la variable de entorno: {var}")

# Asignar las variables de entorno a constantes para ser usadas en el código
API_KEY = os.getenv('SINRIC_API_KEY')
DEVICE_ID = os.getenv('SINRIC_DEVICE_ID')
PORTAL_ID = os.getenv('SINRIC_PORTAL_ID')
TOKEN_ID = os.getenv('SINRIC_TOKEN_ID')

# Función que genera los encabezados para la solicitud HTTP
def get_headers():
    return {
        'Authorization': f'Bearer {TOKEN_ID}',  # Token de autenticación
        'Content-Type': 'application/json'  # Indica que el contenido será en formato JSON
    }

# Ruta principal que sirve la página de inicio (index.html)
@app.route('/')
def index():
    return render_template('index2.html')

# Ruta que maneja la solicitud POST cuando se presiona el timbre
@app.route('/timbre', methods=['POST'])
def doorbell():
    # Base URL de la API de Sinric
    base_url = 'https://api.sinric.pro/api/v1/devices'
    # Endpoint para la acción del dispositivo específico
    endpoint = f'{base_url}/{DEVICE_ID}/action'
    
    # Obtener el tiempo actual en formato Unix timestamp
    created_at = int(time.time())

    # Parámetros para la URL de la solicitud
    params = {
        'clientId': PORTAL_ID,  # ID del portal
        'messageId': API_KEY,   # API Key utilizada como ID de mensaje
        'type': 'event',        # Tipo de evento
        'action': 'DoorbellPress',  # Acción específica (puede ser un evento como "presionar el timbre")
        'createdAt': created_at,   # Tiempo cuando se creó el evento
    }

    # Construcción de la URL con los parámetros
    url = f"{endpoint}?clientId={params['clientId']}&messageId={params['messageId']}&type={params['type']}&action={params['action']}&createdAt={params['createdAt']}"
    print(f"Llamando a la URL: {url}")

    # Datos que se envían en el cuerpo de la solicitud (indicando que el timbre ha sido presionado)
    data = {
        'type': "event",         # Tipo de evento
        'action': 'DoorbellPress',  # Acción del evento
        'value': '{"state": "pressed"}'  # Estado del timbre (se pasó como cadena JSON)
    }
    print(f"Datos enviados en el cuerpo: {data}")

    try:
        # Enviar la solicitud POST a la API de Sinric con los encabezados y los datos
        response = requests.post(url, headers=get_headers(), json=data)

        # Verificar si la respuesta es exitosa
        if response.status_code == 200:
            try:
                response_json = response.json()  # Intentar analizar la respuesta como JSON
                # Retornar una respuesta exitosa con la respuesta de Sinric
                return jsonify({"status": "success", "message": "Timbre presionado correctamente", "response": response_json}), 200
            except json.JSONDecodeError as e:
                # Si no se puede decodificar la respuesta como JSON, manejar el error
                print(f"Error al decodificar JSON: {e}")
                print(f"Contenido de la respuesta: {response.text}")
                return jsonify({"status": "error", "message": "Respuesta JSON no válida de Sinric"}), 500
        else:
            # Si la respuesta no es exitosa (status distinto de 200), mostrar el error
            print(f"La API de Sinric devolvió un error: {response.status_code}")
            print(f"Contenido de la respuesta: {response.text}")
            return jsonify({"status": "error", "message": f"Error al llamar al timbre: {response.text}"}), response.status_code

    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud (por ejemplo, problemas de red o de conexión)
        print(f"Ocurrió un error de solicitud: {e}")
        return jsonify({"status": "error", "message": f"Error al llamar al timbre: {e}"}), 500

# Iniciar la aplicación en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)
