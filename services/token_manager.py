from datetime import datetime, timedelta
from dotenv import load_dotenv

import threading
import requests
import logging
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()


class TokenManager:
    def __init__(self):
        # Keycloak Configuration
        self.realm = os.getenv('KEYCLOAK_REALM')
        self.client_id = os.getenv('KEYCLOAK_CLIENT')
        self.keycloak_url = os.getenv('KEYCLOAK_URL')
        self.client_secret = os.getenv('KEYCLOAK_SECRET')

        self.token: str = None
        self.lock = threading.Lock()
        self.token_expires_at: datetime = None

    def get_token(self):
        with self.lock:
            # Comprobamos si el token existe y esta en fecha
            if self.token and self.token_expires_at > datetime.now():
                return self.token

            # En caso contrario solicitamos un nuevo token a keycloak
            token_url = (f"{self.keycloak_url}/realms/{self.realm}" +
                         "/protocol/openid-connect/token")

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'openid'
            }

            try:
                response = requests.post(
                    token_url,
                    headers=headers,
                    data=data,
                    verify=False,
                    timeout=30
                )
                response.raise_for_status()

                token_data = response.json()
                self.token = token_data['access_token']

                # Calculamos el tiempo de expiracion (con 30s de margen)
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires_at = (datetime.now() +
                                         timedelta(seconds=expires_in - 30))

                logging.info("Token obtenido exitosamente." +
                             f"Expira en {self.token_expires_at} segundos")
                return self.token

            except requests.exceptions.RequestException as e:
                logging.error(f"Error obteniendo el token de Keycloak: {e}")
                raise


if __name__ == '__main__':
    manager = TokenManager()
    token = manager.get_token()
    print(token)
