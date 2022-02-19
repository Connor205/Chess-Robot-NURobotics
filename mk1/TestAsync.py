from time import sleep
from Arduino import Arduino
import serial

from ViewClass import View
from GameLogic import GameLogic
from BasicStockfishPlayers import BasicStockfishPlayers

v = View(BasicStockfishPlayers())

v.gameLoop()