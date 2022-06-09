from ViewClass import View
from BasicStockfishPlayers import BasicStockfishPlayers
from MovementStockfishPlayers import MovementStockfishPlayers
from PlayerVStockfishManual import PlayerVStockfishManual
from PlayerVsStockfishVision import PlayerVsStockfishVision

v = View(
    PlayerVsStockfishVision("/dev/cu.usbmodem142101", "model.h5", rating=3500))
# v = View(PlayerVStockfishManual("/dev/cu.usbmodem143201", rating=500))

v.gameLoop()