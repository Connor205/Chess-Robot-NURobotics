import serial

ser = serial.Serial('/dev/cu.usbmodem142101')  # open serial port

while True:
    # Get user input and set it over serial
    i = input("Enter your input: ")
    ser.write(i.encode())
