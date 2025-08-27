from dotenv import load_dotenv

import requests
import os

load_dotenv()


class Sender:
    def __init__(self):
        self.url: str = os.getenv("APIGATEWAY_URL")

    def send_to_api_gateway(self, msg) -> str:
        """
        Procesa el mensaje y lo envía al API Gateway
        """
        try:
            # Decodificar el payload
            payload = msg.payload.decode('utf-8')
            print(f"Payload recibido: {payload}")

            # Parsear el payload
            properties = payload.split(',')

            # Extraer nombre del sensor
            sensor_name_bad = properties[0].split(':')[1].strip()
            sensor_name = sensor_name_bad.strip('"')

            # Extraer lectura
            lectura_str = properties[1].split(':')[1].strip()
            lect = lectura_str.rstrip('}').strip()

            # Convertir a float
            lectura_parse = lect.replace(',', '.')
            lectura = float(lectura_parse)
            rounded_reading = round(lectura, 6)

            # Preparar datos
            data = {
                "sensorname": sensor_name,
                "lectura": rounded_reading
            }

            # Realizar petición HTTP
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                self.url, json=data, headers=headers, timeout=10, verify=False)
            # response.raise_for_status()  # Lanza excepción si hay error HTTP

            return response.text

        except Exception as e:
            print(f"Error en send_to_api_gateway: {e}")
            raise
