import machine, network, time, urequests, math
from dht import DHT11
from machine import Pin,ADC 
from utime import sleep_ms




#-------------------------[OBJETOS]--------------------------#
url = "https://api.thingspeak.com/update?api_key=0GELCLDC64OALAO0"
#-------------------------[HIGROMETROS]--------------------------#
Fc_suelo_cen = ADC(Pin(36, Pin.IN))
Fc_suelo_izq = ADC(Pin(39, Pin.IN))
Fc_suelo_der = ADC(Pin(34, Pin.IN))
Fc_superficie = ADC(Pin(35,Pin.IN))


Fc_suelo_cen.atten(ADC.ATTN_11DB)
Fc_suelo_izq.atten(ADC.ATTN_11DB)
Fc_suelo_der.atten(ADC.ATTN_11DB)
Fc_superficie.atten(ADC.ATTN_11DB)
#-------------------------[LDR]--------------------------#
ldr = ADC(Pin(32, Pin.IN))
ldr.atten(ADC.ATTN_11DB)

#-------------------------[DHT]--------------------------#
dht= DHT11(Pin(26, Pin.IN))
#-------------------------[RELEE]------------------------#
RELEE = Pin(2, Pin.OUT)
RELEE.value(1)
#-------------------------[Matriz Led]------------------------#
n = 12
p = 5
np = neopixel.NeoPixel(machine.Pin(p), n)
#-------------------------[Conexión WIFI]--------------------------#
print("-----------Conectando al Wifi-----------", end="\n")
sta_if =network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('SSDID', 'password')
while not sta_if.isconnected():
  print(".",end="")
  time.sleep(0.1)
print("Conectado!")


#-------------------------[Lectura de sensores]--------------------------#


def dht_f():

      dht.measure()
      time.sleep(1.1)
      temp = dht.temperature()
      hum = dht.humidity()
      respuesta = urequests.get(url + "&field3=" + str(hum) + "&field2=" + str(temp))
      print ("Respuesta: " + str(respuesta.status_code))
      respuesta.close ()
      print( 'la Humedad de la superficie es: %3.1f ' %hum)
      print( 'la Temperatura de la superficie es: %3.1f C' %temp)
      

def Ldr():
    ldrvalue = ldr.read()
    respuesta = urequests.get(url + "&field5=" + str(ldrvalue))
    print ("Respuesta: " + str(respuesta.status_code))
    respuesta.close ()
    print( 'el nivel de luz es: %3.1f ' %ldrvalue)
    return ldrvalue
    
def hidrometro():
    fcvalueder = Fc_suelo_der.read()
    fcvaluecen = Fc_suelo_izq.read()
    fcvalueizq = Fc_suelo_cen.read()
    fcvaluesuper = Fc_superficie.read()

    fcpromedio = (fcvalueder + fcvaluecen + fcvalueizq + fcvaluesuper) /4

    respuesta = urequests.get(url + "&field1=" + str(fcpromedio))
    print ("Respuesta: " + str(respuesta.status_code))
    respuesta.close ()
    print( 'la humedad en la tierra es: %3.0f ' %fcpromedio)
    return fcpromedio
   
#-------------------------[Rele]--------------------------#
def Relee():
    if hidrometro() >= 3200:
        RELEE.value (0)
        respuesta = urequests.get(url + "&field4=" + str(RELEE.value()))
        print ("Respuesta: " + str(respuesta.status_code))
        respuesta.close ()
        print( 'Estado Riego: '  +str(RELEE.value()))
    else:
        RELEE.value (1)
        respuesta = urequests.get(url + "&field4=" + str(RELEE.value()))
        print ("Respuesta: " + str(respuesta.status_code))
        respuesta.close ()
        print( 'Estado Riego: ' +str(RELEE.value()))


#-------------------------[Matiz Led]--------------------------#
def led():
    if ldr() <200 :
        np[0] = (0, 0, 255)
        np[1] = (255, 0, 0)
        np[2] = (0, 0, 255)
        np[3] = (255, 0, 0)
        np[4] = (0, 0, 255)
        np[5] = (255, 0, 0)
        np[6] = (0, 0, 255)
        np[7] = (255, 0, 0)
        np[8] = (0, 0, 255)
        np[9] = (255, 0, 0)
        np[10] = (0, 0, 255)
        np[11] = (255, 0, 0)
        np.write()
    else:
        np[0] = (0, 0, 0)
        np[1] = (0, 0, 0)
        np[2] = (0, 0, 0)
        np[3] = (0, 0, 0)
        np[4] = (0, 0, 0)
        np[5] = (0, 0, 0)
        np[6] = (0, 0, 0)
        np[7] = (0, 0, 0)
        np[8] = (0, 0, 0)
        np[9] = (0, 0, 0)
        np[10] = (0, 0, 0)
        np[11] = (0, 0, 0)
        np.write()
#-------------------------[salidas]--------------------------#
while True:
    dht_f()
    sleep_ms(10000)
    Ldr()
    sleep_ms(10000)
    led()
    sleep_ms(10000)
    hidrometro()
    sleep_ms(10000)
    Relee()
    sleep_ms(1800000)