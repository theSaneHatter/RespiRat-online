from machine import Pin, Timer, UART, ADC
import time
import network
import rp2, sys, socket

led = Pin("LED",Pin.IN)
def tick(timer):
    global led
    led.toggle()
tim = Timer()
#tim.init(freq=1,mode=Timer.PERIODIC, callback=tick)
for i in range(6):
    led.toggle()
    time.sleep(1/6)

SSID = "sixseven"
passwd = "ac88cd112"

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


def connect(ssid, password):
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
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    page = f"""
 <!DOCTYPE html>
<html>
<body>
<form action="./lighton">
<input type="submit" value="Light on" />
</form>
<h1>.</h1>
<form action="./lightoff">
<input type="submit" value="Light off" />
</form>
<h1>.</h1>
<form action="./close">
<input type="submit" value="Stop server" />
</form>
<p>LED is {state}</p>
<p>Temperature is {temperature}</p>
</body>
</html></h1>
    """
    return page

def get_temp():
    sensor_temp = ADC(4)
    temp = sensor_temp.read_u16()
    vpd = (3.3/65535)
    reading = vpd*temp
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    return temperature

def serve(connection):
    #Start a web server
    state = 'ON'
    temperature = 0
    pico_led = Pin("LED",Pin.IN)

    while true:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if '/lighton' in request:
            pico_led.on()
            state = 'on'
        elif '/lightoff' in request:
            pico_led.off()
            state = 'off'
        elif '/close' in request:
            sys.exit()
        temperature = get_temp()
        html = webpage(temperature, state)

        client.send(html)
        client.close()
#   tim = timer()
#   tim.init(freq=30, mode=timer.periodic,callback=manage_request)
    print("started socket manager")

def serve_tick(timer):
    state = 'ON'
    temperature = 0
    pico_led = Pin("LED",Pin.IN)

    client = connection.accept()[0]
    request = client.recv(1024)
    request = str(request)
    try:
        request = request.split()[1]
    except IndexError:
        pass
    if '/lighton' in request:
        pico_led.on()
        state = 'on'
    elif '/lightoff' in request:
        pico_led.off()
        state = 'off'
    elif '/close' in request:
        sys.exit()
    temperature = get_temp()
    html = webpage(temperature, state)

    client.send(html)
    client.close()
#   tim = timer()
#   tim.init(freq=30, mode=timer.periodic,callback=manage_request)
    print("started socket manager")


ip = host(SSID, passwd)
connection = open_socket(ip)
#serve(connection)



