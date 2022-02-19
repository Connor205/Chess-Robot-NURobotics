from time import sleep
from Arduino import Arduino
import serial

from ViewClass import View
from GameLogic import GameLogic
from BasicStockfishPlayers import BasicStockfishPlayers

# port = "/dev/tty.usbmodem143201"

# # Continously read from state of a serial port
# def readSerial(port):
#     ser = serial.Serial(port, 9600, timeout=None)
#     while True:
#         try:
#             input = ser.read_until(b'\n').decode('utf-8')
#             print(f'Arduino - {input}')
#         except UnicodeDecodeError:
#             print("UnicodeDecodeError")

#         sleep(0.1)

# A = Arduino(port)

# while True:
#     print(A.state)
#     sleep(5)

v = View(BasicStockfishPlayers())
