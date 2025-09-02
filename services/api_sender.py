from services.token_manager import TokenManager

from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

import requests
import tempfile
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()


class Sender:
    def __init__(self):
        self.url: str = os.getenv("APIGATEWAY_URL")
        # Contraseña del certificado ayeserver.pfx
        self.pfx_password: str = os.getenv("CERTIFICATE_PASSWORD")
        self.tokenManager = TokenManager()

    def _extract_cert_and_key_from_pfx(
        self,
        pfx_path: str,
        password: str = None
    ):
        """
        Extrae el certificado y la clave privada de un archivo .pfx
        Retorna rutas temporales de los archivos .pem
        """
        try:
            with open(pfx_path, 'rb') as pfx_file:
                pfx_data = pfx_file.read()

            # Decodificar el archivo .pfx
            private_key, certificate, _ = pkcs12.load_key_and_certificates(
                pfx_data,
                password.encode('utf-8') if password else None
            )

            # Crear archivos temporales
            cert_temp = tempfile.NamedTemporaryFile(
                mode='wb', suffix='.pem', delete=False)
            key_temp = tempfile.NamedTemporaryFile(
                mode='wb', suffix='.pem', delete=False)

            # Escribir certificado
            cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
            cert_temp.write(cert_pem)
            cert_temp.close()

            # Escribir clave privada
            key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            key_temp.write(key_pem)
            key_temp.close()

            return cert_temp.name, key_temp.name

        except Exception as e:
            print(f"Error al extraer certificado del archivo .pfx: {e}")
            raise

    def send_to_api_gateway(self, msg) -> str:
        """
        Procesa el mensaje y lo envía al API Gateway usando certificado cliente
        """
        cert_temp = None
        key_temp = None

        try:
            token = self.tokenManager.get_token()

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

            # Preparar certificado cliente
            # Subir un nivel desde services/ hasta la raíz del proyecto,
            # luego entrar a https/
            project_root = os.path.dirname(os.path.dirname(__file__))
            pfx_path = os.path.join(project_root, 'https', 'ayeserver.pfx')

            if not os.path.exists(pfx_path):
                raise FileNotFoundError(
                    f"No se encontró el archivo de certificado en: {pfx_path}")

            # Extraer certificado y clave del .pfx
            cert_temp, key_temp = self._extract_cert_and_key_from_pfx(
                pfx_path, self.pfx_password
            )

            # Realizar petición HTTP con certificado cliente
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            response = requests.post(
                self.url,
                json=data,
                headers=headers,
                timeout=10,
                cert=(cert_temp, key_temp),  # Certificado cliente
                verify=False  # Mantener False para certificados autofirmados
            )

            return response.text

        except Exception as e:
            print(f"Error en send_to_api_gateway: {e}")
            raise

        finally:
            # Limpiar archivos temporales
            if cert_temp and os.path.exists(cert_temp):
                try:
                    os.unlink(cert_temp)
                except Exception:
                    pass

            if key_temp and os.path.exists(key_temp):
                try:
                    os.unlink(key_temp)
                except Exception:
                    pass
