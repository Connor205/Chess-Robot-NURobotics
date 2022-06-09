import threading
import time
from ArduinoState import ArduinoState
import serial
import logging
import sys


class Arduino:
    state = ArduinoState()
    port = None
    baud = None
    ser = None
    stateLock = threading.Lock()
    logger = None

    def __init__(self, port: str, baud=9600):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.port = port
        self.baud = baud
        self.connect()
        self.monitorState()

    def connect(self):
        # Start up the serial connection
        self.ser = serial.Serial(self.port, self.baud, timeout=None)
        self.ser.flushInput()
        self.ser.flushOutput()

    def monitorState(self):
        # Start a thread to monitor the state of the Arduino
        self.t = threading.Thread(target=self.monitorArduinoOutputThread,
                                  daemon=True)
        self.t.start()

    def monitorArduinoOutputThread(self):
        # This is the thread that monitors the state of the Arduino
        while True:
            # Read the state of the Arduino
            self.readInput()
            # Sleep for a bit
            time.sleep(0.1)

    def readInput(self) -> None:
        # Read the state of the Arduino
        # Pipes the output into self.state
        # This is a blocking call
        try:
            input = self.ser.read_until(b'\n').decode('utf-8').strip()
            self.logger.info(f'Arduino Output --{input}--')
            command, value = input.split(':')
            print("Command: {} | Value: {}".format(command, value))
            if command == 'STATE':
                with self.stateLock:
                    self.state.state = value
                print("Updated Arduino State to: {}".format(value))
            elif command == 'x_pos':
                with self.stateLock:
                    self.state.x_pos = int(value)
            elif command == 'y_pos':
                with self.stateLock:
                    self.state.y_pos = int(value)
            elif command == 'z_pos':
                with self.stateLock:
                    self.state.z_pos = int(value)
            elif command == 'grabber_state':
                with self.stateLock:
                    self.state.grabber_state = value
        except UnicodeDecodeError:
            print("UnicodeDecodeError")

    def getStateSafe(self):
        # getter for state with locking
        with self.stateLock:
            return self.state

    def sendCommand(self, type: str, values: list = []) -> None:
        # If the character : is in any of the strings in values raise an exception
        values = [str(value) for value in values]
        for value in values:
            if ':' in value:
                raise (ValueError(
                    'Values cannot contain the character : when sending data to the Arduino: {}'
                    .format(value)))

        # Here we write the type of command and then the value of said command so that the arduino is able to parse it
        self.ser.write(f'{type}\n'.encode())
        time.sleep(.2)
        for value in values:
            self.ser.write(f'{value}\n'.encode())
            time.sleep(.2)

    def waitForReady(self):
        if self.state.state == 'ready':
            print("State Was Ready When Wait For Ready Was Called")
        time.sleep(.3)
        while self.state.state != 'ready':
            time.sleep(0.1)

    def waitForHome(self):
        if self.state.state == 'home':
            print("State Was Home When Wait For Home Was Called")
        time.sleep(.3)
        while self.state.state != 'home':
            time.sleep(0.1)
