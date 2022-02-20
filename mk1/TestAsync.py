from time import sleep
import serial

from ViewClass import View
from GameLogic import GameLogic
from BasicStockfishPlayers import BasicStockfishPlayers

v = View(BasicStockfishPlayers())

v.gameLoop()