import Arduino
import time
import threading
import logging
import sys

import serial

A = Arduino.Arduino("/dev/cu.usbmodem142101")

while True:
    # Get user input and set it over serial
    i = input("Enter your type: ")
    data = input("Enter your data comma seperated: ").split(',')
    A.sendCommand(i, data)
