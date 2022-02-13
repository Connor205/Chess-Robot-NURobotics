from ast import Raise
import threading
import time
import os
from ArduinoState import ArduinoState
import serial
import logging

class Arduino:
    state = ArduinoState()
    port = None
    baud = None
    ser = None
    stateLock = threading.Lock()
    logger = None

    def __init__(self, port: str, baud=9600):
        self.logger = logging.getLogger(__name__)
        self.port = port
        self.baud = baud
        self.connect()
        self.monitorState()

    def connect(self):
        # Start up the serial connection
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        self.ser.flushInput()
        self.ser.flushOutput()

    def monitorState(self):
        # Start a thread to monitor the state of the Arduino
        self.t = threading.Thread(target=self.monitorArduinoOutputThread, daemon=True)
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
        input = self.ser.readline().decode('utf-8').rstrip()

        self.logger.info(f'Arduino: {input}')
        command, value = input.split(':')
        match command:
            case 'state':
                with self.stateLock:
                    self.state.state = value
            case 'x_pos':
                with self.stateLock:
                    self.state.x_pos = int(value)
            case 'y_pos':
                with self.stateLock:
                    self.state.y_pos = int(value)
            case 'z_pos':
                with self.stateLock:
                    self.state.z_pos = int(value)
            case 'grabber_state':
                with self.stateLock:
                    self.state.grabber_state = value
        
    def getStateSafe(self):
        # getter for state with locking
        with self.stateLock:
            return self.state

    def sendCommand(self, type: str, value: str) -> None:
        if ':' in value:
            Raise(ValueError('Value cannot contain a colon when sending data to the Arduino'))
        self.ser.write(f'{type}:{value}\n'.encode('utf-8'))
    
    def waitForReady(self):
        while self.state.state != 'ready':
            time.sleep(0.1)

    
        
