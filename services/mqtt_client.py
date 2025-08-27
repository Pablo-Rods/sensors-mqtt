from services.api_sender import Sender
from dotenv import load_dotenv

import paho.mqtt.client as mqtt

import threading
import uuid
import os

load_dotenv()


class MQTTClient:
    def __init__(self):
        self.broker: str = os.getenv("BROKER_HOST")
        self.port: int = int(os.getenv("BROKER_PORT"))
        self.topic: str = os.getenv("BROKER_TOPIC")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.sender: Sender = Sender()
        self.client = None

    def start_connection(self):
        """
        Establece la conexión con el broker MQTT
        """
        try:
            client_id = str(uuid.uuid4())

            # Crear cliente MQTT
            self.client = mqtt.Client(client_id=client_id)

            # Configurar credenciales
            self.client.username_pw_set(self.username, self.password)

            # Configurar callbacks
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.on_disconnect = self._on_disconnect

            # Conectar al broker
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()

            print("Successfully connected")

        except Exception:
            raise Exception(
                f"Failed to connect to broker {self.broker}:{self.port}")

    def subscribe(self):
        """
        Se suscribe a un topic específico
        """
        try:
            self.client.subscribe(self.topic)
            print(f"Suscrito al topic: {self.topic}")
        except Exception:
            raise Exception(
                f"Couldn't subscribe to the given topic: {self.topic}")

    def disconnect(self):
        """Desconecta el cliente"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        """Callback cuando se conecta al broker"""
        if rc == 0:
            print("Conexión establecida exitosamente")
        else:
            print(f"Error de conexión: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback cuando se desconecta"""
        print("Desconectado del broker")

    def _on_message(self, client, userdata, msg):
        """Callback cuando se recibe un mensaje"""
        try:
            # Procesar en un hilo separado para no bloquear el callback
            threading.Thread(target=self._handle_message,
                             args=(msg,), daemon=True).start()
        except Exception as e:
            print(f"Error procesando mensaje: {e}")

    def _handle_message(self, msg):
        """Maneja el mensaje en un hilo separado"""
        try:
            response = self.sender.send_to_api_gateway(msg)
            print(f"Posted to database {response}")
        except Exception as e:
            print(f"Error enviando a API Gateway: {e}")
