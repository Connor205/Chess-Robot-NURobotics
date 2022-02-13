from time import sleep
from Arduino import Arduino

A = Arduino("/dev/ttyACM0")

n = 1
while (True):
    A.sendCommand("state", "{n}")
    sleep(2)
    n += 1
