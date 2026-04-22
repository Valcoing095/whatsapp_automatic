# WhatsApp Sender - Documentación de Instalación y Uso

Sistema automatizado para envío masivo de mensajes de WhatsApp a través de WhatsApp Web, utilizando Selenium y Flask.

## Requisitos Previos

### 1. Dependencias del Sistema

- **Python 3.8+** - [Descargar](https://www.python.org/downloads/)
- **Google Chrome** - [Descargar](https://www.google.com/chrome/)
- **Node.js 18+** (opcional, para enviar_whatsapp_auto.js)
- **ChromeDriver** compatible con tu versión de Chrome

### 2. Verificar Instalación de Chrome

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Linux
google-chrome --version
```

Anota la versión para descargar el ChromeDriver correspondiente.

---

## Instalación

### Paso 1: Clonar o descargar el proyecto

```bash
cd /Users/usuario1/Desktop/opencodeProject
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### Paso 3: Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### Paso 4: Instalar dependencias de Node.js (opcional)

```bash
npm install
```

---

## Estructura del Proyecto

```
opencodeproject/
├── app.py                    # Aplicación Flask principal
├── whatsapp_sender.py       # Clase Python para envío
├── enviar_whatsapp_auto.js   # Script Node.js alternativo
├── crear_ejemplo.py          # Genera Excel de prueba
├── requirements.txt          # Dependencias Python
├── templates/
│   └── index.html           # Interfaz web
├── uploads/                  # Archivos Excel subidos
└── clientes_ejemplo.xlsx    # Excel de ejemplo
```

---

## Uso Rápido (Opción 1: Interfaz Web)

### Paso 1: Ejecutar la aplicación

```bash
python app.py
```

### Paso 2: Abrir en navegador

Visita: **http://localhost:5000**

### Paso 3: Subir archivo Excel

El Excel debe tener las columnas:
- `nombre` - Nombre del cliente
- `celular` - Número de teléfono (10 dígitos, sin código de país)
- `placa` - Número de placa

### Paso 4: Configurar mensaje

Usa las variables:
- `{nombre}` - Nombre del cliente
- `{celular}` - Teléfono del cliente
- `{placa}` - Placa del vehículo

Ejemplo:
```
Hola {nombre}, te informamos que tu placa {placa} tiene un pendiente.
```

### Paso 5: Iniciar WhatsApp Web

1. Clic en "Iniciar WhatsApp Web"
2. Se abrirá Chrome con WhatsApp Web
3. Escanea el código QR con tu WhatsApp
4. Clic en "Ya escaneé el QR"

### Paso 6: Enviar mensajes

Clic en "Enviar Mensajes" y observa el progreso.

---

## Uso por Línea de Comandos (Opción 2: Python)

### Crear archivo Excel de prueba

```bash
python crear_ejemplo.py
```

Esto genera `clientes_ejemplo.xlsx`.

### Usar la clase WhatsAppSender

```python
from whatsapp_sender import WhatsAppSender

sender = WhatsAppSender()
sender.start()

# Esperar QR y conexión...
sender.send_message("3022475080", "Hola Juan!")
sender.close()
```

---

## Uso con Node.js (Opción 3)

```bash
node enviar_whatsapp_auto.js
```

Modifica las líneas en `enviar_whatsapp_auto.js`:
```javascript
const number = '573022475080';
const message = 'Hola! Este es un mensaje automático.';
```

---

## Dependencias

### Python (requirements.txt)

| Paquete | Versión | Descripción |
|---------|---------|--------------|
| flask | 3.0.0 | Framework web |
| openpyxl | 3.1.2 | Lectura de archivos Excel |
| selenium | 4.15.0 | Automatización del navegador |
| webdriver-manager | 4.0.1 | Gestión automática de ChromeDriver |

### Node.js (package.json)

| Paquete | Versión | Descripción |
|---------|---------|--------------|
| whatsapp-web.js | 1.34.6 | API para WhatsApp Web |
| qrcode | 1.5.4 | Generación de códigos QR |

---

## Solución de Problemas

### Error: "Chrome not reachable"

1. Verifica que Chrome esté instalado
2. Confirma que la ruta en `app.py` es correcta:
   ```python
   options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   ```

### Error: "Session not created"

1. Desinstala ChromeDriver antiguo
2. Deja que webdriver-manager lo maneje automáticamente
3. O descarga el ChromeDriver que coincida con tu versión de Chrome

### Error: "No such file or directory: 'uploads'"

```bash
mkdir uploads
```

### WhatsApp Web no responde

1. Asegúrate de estar logueado en WhatsApp Web
2. Verifica que el número tenga el formato correcto (código de país + número)
3. Aumenta los `time.sleep()` si tu conexión es lenta

---

## Formato de Números de Teléfono

El sistema agrega automáticamente el código de país:

| Entrada | Formato |
|---------|---------|
| 3022475080 | 573022475080 |
| 302247508 | 5302247508 |

Para números internacionales, incluye el código:
- Colombia: `57` + número
- Ejemplo: `573022475080`

---

## Notas de Seguridad

- **No compartas** tu archivo `requirements.txt` con credenciales
- **Mantén sesión** de WhatsApp activa para evitar re-autenticación
- **Limita** la velocidad de envío para evitar bloqueos

---

## Licencia

ISC
