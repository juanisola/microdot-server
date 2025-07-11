# Aplicacion del servidor
from microdot import Microdot, Response
import network
from time import sleep
from machine import Pin, SoftI2C
import ssd1306

# Configuración I2C para OLED (verifica tus pines)
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))  # Pines comunes en ESP32
oled = ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)  # Dirección común 0x3C o 0x3D

# Función para conectar al WiFi
def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Conectando a la red...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print(".", end="")
            sleep(0.5)
    print('Configuración de red:', sta_if.ifconfig())
    return sta_if.ifconfig()[0]  # Usamos [0] para la IP local

WIFI_SSID = "Cooperadora Alumnos"
WIFI_PASSWORD = "" 

try:
    ip = connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    
    # Mostrar IP en OLED
    oled.fill(0)
    oled.text("Accede con", 0, 0)
    oled.text(ip, 0, 12)
    oled.show()
except Exception as e:
    print("Error en OLED o WiFi:", e)

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    with open('index.html', 'r') as file:
        html = file.read()
    
    # Variables a reemplazar en el HTML
    variables = {
        '{{#}}': "Actividad 01 - Microdot",  # Nota: mayúscula en HTML
        '{{Mensaje}}': "Mi primer server de Microdot",
        '{{Alumno}}': "Juan Cruz Isola"  # Nota: mayúscula en HTML
    }
    
    for placeholder, valor in variables.items():
        html = html.replace(placeholder, valor)
    
    return html
@app.route('/styles/base.css')
def serve_css(request):
    with open('styles/base.css', 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/css'}

@app.route('/scripts/base.js')
def serve_js(request):
    with open('scripts/base.js', 'r') as f:
        return f.read(), 200, {'Content-Type': 'application/javascript'}
app.run(host=ip, port=80, debug=True)
