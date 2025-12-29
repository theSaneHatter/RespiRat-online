from phew import server, connect_to_wifi
from machine import Pin, ADC
import time
import network
import _thread
import socket
import microdot
import ntptime
import ujson
import random

led = Pin('LED', Pin.IN)
for i in range(12):
    led.toggle()
    time.sleep(1/12)

def read_adc(n):
    pin = ADC(n)
    value = pin.read_u16()
    return value

def get_temp():
    sensor_temp = ADC(4)
    temp = sensor_temp.read_u16()
    vpd = (3.3/65535)
    reading = vpd*temp
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    return temperature

def set_time():
    print(f'attempting to set time')
    tns = True
    while tns:
        try:
            ntptime.settime()
            tns = False
        except OSError:
            print('failed to set time...')
        except:
            print('an unpredicted error occured while setting time.\nThrowing!')
            raise
    print(f'time set!>{time.time()}<')

def host(ssid, passwd):
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    if ssid == "" or ssid == None:
        wlan.config(essid=ssid, security=0)
    else:
        wlan.config(essid=ssid, password=passwd)
 #   while not wlan.isconnected():
 #      print('waiting for conection...')
 #      time.sleep(1)
    print(wlan.ifconfig())
    print(f'hosting network ssid:>{ssid}<, passwd:>{passwd}<')
    ip = wlan.ifconfig()[0]
    return ip

def connect(ssid, password, settime=False):
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print(f'Waiting for connection >{ssid}<...')
        time.sleep(0.5)
        Pin('LED', Pin.IN).toggle()
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    if settime:
        set_time()

    return ip

connect("MostlyWideFeet", "QB@YZU$88J9a2!", settime=True)

def json_response(obj, code=200):
    return ujson.dumps(obj), code, {
        "Content-Type": "application/json"
    }

@server.route("/test", methods=["GET"])
def random_number(request):
  min = int(request.query.get("min", 0))
  max = int(request.query.get("max", 100))
  return str(random.randint(min, max))

@server.route('/', methods=['GET'])
def webpage(request):
    with open('index.html','r') as f:
        contents = f.read()
    return str(contents)

@server.route('/main.js')
def serve_js(request):
    with open('main.js') as f:
        return f.read(), 200, {"Content-Type": "application/javascript"}

@server.route('/temp', methods=['GET'])
def serve_temp(request):
    temp = get_temp()
    return str(temp)

@server.route('/adc')
def serve_adc(request):
    # value = read_adc(0)
    value = random.randint(0,1000)
    tim = round(time.time())
    obj = {"time":tim, "value":int(value)}
    print(f'@debug:sent obj {obj}')
    return json_response(obj)

@server.route('/lightoff')
def lightoff(request):
    print('@debug:user tried to turn light off')
    Pin("LED", Pin.OUT).value(0)
    return '0'

@server.route('/lighton')
def lighton(request):
    print('@debug:user tried to turn light on')
    Pin("LED", Pin.OUT).value(1)
    return '1'

@server.catchall()
def catchall(request):
    return "Not found", 404



server.run(host='0.0.0.0', port=80)
