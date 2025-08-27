from services.mqtt_client import MQTTClient

import time


def start_server():
    """
    Inicia el servidor MQTT y se mantiene en ejecución
    """
    client = MQTTClient()

    client.start_connection()
    client.subscribe()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo cliente MQTT...")
        client.disconnect()


if __name__ == '__main__':
    start_server()
