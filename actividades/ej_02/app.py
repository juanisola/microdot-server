from microdot import Microdot, Response
import network
from time import sleep
from machine import Pin, SoftI2C
import ssd1306
from neopixel import NeoPixel

# Configuración I2C para OLED
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

# Configuración de LEDs simples
led1 = Pin(32, Pin.OUT)
led2 = Pin(33, Pin.OUT)
led3 = Pin(25, Pin.OUT)

# Inicializar LEDs apagados
led1.value(0)
led2.value(0)
led3.value(0)

# Configuración de NeoPixels
np = NeoPixel(Pin(27), 4)  
for i in range(4):
    np[i] = (255, 255, 255)  # Inicializar en blanco
np.write()

# Función WIFI
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
    return sta_if.ifconfig()[0]

# WIFI
WIFI_SSID = "Cooperadora Alumnos"
WIFI_PASSWORD = ""

try:
    ip = connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    oled.fill(0)
    oled.text("Accede con:", 0, 0)
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
    
    variables = {
        '{{#}}': "Actividad 02 - Microdot",
        '{{Mensaje}}': "Control de LEDs",
        '{{Alumno}}': "Juan Cruz Isola"
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

@app.route('/led/<led_num>/toggle')
def toggle_led(request, led_num):
    try:
        led_num = int(led_num)
        if led_num == 1:
            led1.value(not led1.value())
            return str(led1.value())
        elif led_num == 2:
            led2.value(not led2.value())
            return str(led2.value())
        elif led_num == 3:
            led3.value(not led3.value())
            return str(led3.value())
        else:
            return "LED no válido", 400
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/neopixel/<r>/<g>/<b>')
def set_neopixel(request, r, g, b):
    try:
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        
        # Aplicar a todos los LEDs
        for i in range(4):
            np[i] = (r, g, b)
        np.write()
        
        return f"OK: {r},{g},{b}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

app.run(host=ip, port=80, debug=True)