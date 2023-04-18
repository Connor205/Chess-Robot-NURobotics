from ResetMoveGenerator import generateAllResetMoves
from Board import Board
from ResetMoves import ResetMovement
from typing import List
import chess
import random
import neat
# SO the goal of this agent is going to be to generate a list of ResetMoves based on some parameters


def square_from_xy(x: int, y: int):
    return chess.square(x - 3, y)


class ResetAgent:

    def __init__(self, startingBoard: Board):
        self.board = startingBoard
        self.currentPosition = (0, 0)
        self.heldPiece = None

    def generateSeriesOfResetMoves(self) -> List[ResetMovement]:
        # We want to loop until we have reset all of the pieces on the board
        # We can do this by checking if there are any legal reset moves
        movements = []
        possibleMoves = generateAllResetMoves(self.currentPosition, self.board)
        count = 0
        while len(possibleMoves) > 0:
            count += 1
            # print("________________________________________________")
            # print("Count = ", count)
            # print("Board:", self.board)
            assert count < 33
            # We want to find the best move
            bestMove = self.findBestMove(possibleMoves)
            # print("Best Move:", bestMove._moves)
            # We want to execute the best move
            self.executeMove(bestMove)
            # We want to add the move to our list of movements
            movements.append(bestMove)
            # We want to update our list of possible moves
            possibleMoves = generateAllResetMoves(self.currentPosition,
                                                  self.board)
        return movements

    def scoreResetMove(self, move: ResetMovement):
        raise NotImplementedError("This method has not been implemented yet")

    def findBestMove(self, moves: List[ResetMovement]):
        bestMove = None
        bestScore = float("-inf")
        for move in moves:
            score = self.scoreResetMove(move)
            if score > bestScore:
                bestScore = score
                bestMove = move
        return bestMove

    def executeMove(self, move: ResetMovement):
        for m in move._moves:
            if m.isHorizontal():
                self.currentPosition = m.end
            elif m.isVertical():
                pass
            elif m.isPiece():
                if m.type == "pickup":
                    self.heldPiece = self.board.remove_piece(
                        self.currentPosition[1], self.currentPosition[0])
                elif m.type == "place":
                    self.board.set_square(
                        square_from_xy(self.currentPosition[1],
                                       self.currentPosition[0]),
                        self.heldPiece)


class ClosestAgent(ResetAgent):

    def scoreResetMove(self, move: ResetMovement):
        # print("Score: ", move.getFeatureArray(self.currentPosition)[0] * -1)
        return -1 * move.getFeatureArray(self.currentPosition)[0]


class AStartAgent(ResetAgent):

    def scoreResetMove(self, move: ResetMovement):
        # print("Score: ", move.getFeatureArray(self.currentPosition)[2] * -1)
        return -1 * move.getFeatureArray(self.currentPosition)[2]


class RandomAgent(ResetAgent):

    def scoreResetMove(self, move: ResetMovement):
        return random.random()


class NeatAgent(ResetAgent):

    def __init__(self, startingBoard: Board, net):
        super().__init__(startingBoard)
        self.net = net

    def scoreResetMove(self, move: ResetMovement):
        # We want to get the feature array
        featureArray = move.getFeatureArray(self.currentPosition)
        # We want to get the score
        score = self.net.activate(featureArray)[0]
        return score


class FeatureAgent(ResetAgent):

    def __init__(self, startingBoard: Board, weights):
        super().__init__(startingBoard)
        self.weights = weights

    def scoreResetMove(self, move: ResetMovement):
        # We want to get the feature array
        featureArray = move.getFeatureArray(self.currentPosition)
        # We want to get the score
        score = 0
        for i in range(len(featureArray)):
            score += featureArray[i] * self.weights[i]
        return score