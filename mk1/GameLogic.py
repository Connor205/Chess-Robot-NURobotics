class GameLogic:

    def getCurretFenString(self):
        raise NotImplementedError("Method: getCurretFenString not implmented")

    def getPlayerMove(self) -> str:
        raise NotImplementedError("Method: getPlayerMove not implmented")

    def processPlayerMove(self, str):
        raise NotImplementedError("Method: processPlayerMove not implmented")

    def generateComputerMove(self) -> str:
        raise NotImplementedError(
            "Method: generateComputerMove not implmented")

    def makeComputerMove(self, str) -> bool:
        raise NotImplementedError("Method: makeComputerMove not implmented")

    def getLogicName(self):
        raise NotImplementedError("Method: getLogicName not implmented")
