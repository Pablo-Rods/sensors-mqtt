# Cliente MQTT para Sensores IoT

Un cliente MQTT en Python que recibe datos de sensores y los reenvía a un API Gateway para su procesamiento y almacenamiento.

## 📋 Descripción

Este proyecto implementa un cliente MQTT que:

- Se conecta a un broker MQTT usando credenciales
- Se suscribe a un topic específico para recibir datos de sensores
- Procesa los mensajes recibidos (formato JSON con nombre del sensor y lectura)
- Envía los datos procesados a un API Gateway vía HTTP POST
- Maneja errores y desconexiones de forma robusta

## 🏗️ Arquitectura

```
Sensores IoT → Broker MQTT → Cliente MQTT → API Gateway → Base de Datos
```

## 📦 Dependencias

Las dependencias están definidas en `requirements.txt`:

```
python-dotenv == 1.1.1
paho-mqtt == 2.1.0
requests == 2.32.5
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
# Configuración del Broker MQTT
BROKER_HOST=tu-broker-mqtt.com
BROKER_PORT=1883
BROKER_TOPIC=sensores/data
USERNAME=tu-usuario-mqtt
PASSWORD=tu-password-mqtt

# API Gateway
APIGATEWAY_URL=https://tu-api-gateway.com/sensores
```

### Formato de Mensajes MQTT

El cliente espera mensajes en el siguiente formato JSON:

```json
{
  "sensorname": "temperatura_sala_1",
  "lectura": 23.5
}
```

O en formato de cadena separada por comas:

```
"sensorname": "temperatura_sala_1", "lectura": 23,5
```

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd mqtt-sensor-client
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Linux/Mac:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crea el archivo `.env` con tu configuración específica.

### 6. Ejecutar el cliente

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── .env                   # Variables de entorno (no incluido en git)
├── .gitignore            # Archivos ignorados por git
└── services/
    ├── __init__.py       # Paquete de servicios
    ├── mqtt_client.py    # Cliente MQTT principal
    └── api_sender.py     # Servicio para enviar datos al API Gateway
```

## 🔧 Componentes Principales

### MQTTClient (`services/mqtt_client.py`)

- Gestiona la conexión con el broker MQTT
- Maneja suscripciones y callbacks
- Procesa mensajes en hilos separados para evitar bloqueos
- Implementa reconexión automática

### Sender (`services/api_sender.py`)

- Procesa y valida los datos recibidos del MQTT
- Formatea los datos para el API Gateway
- Realiza peticiones HTTP POST con manejo de errores
- Redondea las lecturas a 6 decimales para precisión

## 🛡️ Manejo de Errores

El sistema incluye manejo robusto de errores para:

- Fallos de conexión MQTT
- Errores de parsing de mensajes
- Timeouts de HTTP
- Desconexiones inesperadas

## 📊 Logs y Monitoreo

El cliente imprime información útil:

- Estado de conexión MQTT
- Mensajes recibidos y procesados
- Respuestas del API Gateway
- Errores detallados para debugging

## 🚦 Estados de Ejecución

- **Conexión exitosa**: Se muestra "Successfully connected"
- **Suscripción**: Confirma suscripción al topic
- **Procesamiento**: Muestra payload y respuesta del API
- **Desconexión**: Maneja Ctrl+C para salida limpia

## ⚠️ Notas Importantes

- Mantén seguras las credenciales en el archivo `.env`
- El cliente maneja automáticamente la reconexión en caso de pérdida de conexión
- Los mensajes se procesan de forma asíncrona para mejor rendimiento
- Asegúrate de que el API Gateway esté disponible antes de ejecutar el cliente

## 🆘 Solución de Problemas

### Error de conexión MQTT

- Verifica las credenciales en `.env`
- Confirma que el broker esté disponible
- Revisa la configuración del firewall

### Error al enviar a API Gateway

- Verifica la URL del API Gateway
- Confirma que el servicio esté corriendo
- Revisa los logs para errores HTTP específicos

### Problemas de parsing

- Verifica el formato de los mensajes MQTT
- Confirma que los sensores envíen datos en el formato esperado
