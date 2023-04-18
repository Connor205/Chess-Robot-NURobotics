from typing import Tuple, List
import numpy as np

# A move can either be a 2d movement or a vertical movement

MAX_MM_PER_SECOND = 280
MIN_MM_PER_SECOND = 140
AVERAGE_MM_PER_SECOND = (MAX_MM_PER_SECOND + MIN_MM_PER_SECOND) / 2
PHYSICAL_SQUARE_SIZE = 40


def computeTimeToMove(d: float):
    return (d / 2) / MAX_MM_PER_SECOND + (d / 2) / MIN_MM_PER_SECOND


def euclidDistanceSquares(start: Tuple[int, int], end: Tuple[int,
                                                             int]) -> float:
    return ((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5


def euclidDistanceMM(start: Tuple[int, int], end: Tuple[int, int]) -> float:
    return euclidDistanceSquares(start, end) * PHYSICAL_SQUARE_SIZE


class Move:
    # Distance Traveled
    def getEuclidDistance(self) -> int:
        raise NotImplementedError("This method must be implemented")

    def getManhattanDistance(self) -> int:
        raise NotImplementedError("This method must be implemented")

    def isHorizontal(self) -> bool:
        return False

    def isVertical(self) -> bool:
        return False

    def isPiece(self) -> bool:
        return False

    def getTime(self) -> int:
        raise NotImplementedError("This method must be implemented")


class HorizontalMove(Move):

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        self.start = start
        self.end = end

    def __str__(self):
        return f"Move from {self.start} to {self.end}"

    def __repr__(self):
        return self.__str__()

    def getManhattanDistance(self) -> int:
        return abs(self.start[0] - self.end[0]) + abs(self.start[1] -
                                                      self.end[1])

    def getEuclidDistance(self) -> int:
        return euclidDistanceSquares(self.start, self.end)

    def getTime(self) -> int:
        return computeTimeToMove(self.getEuclidDistance() *
                                 PHYSICAL_SQUARE_SIZE)

    def isHorizontal(self) -> bool:
        return True

    def isVertical(self) -> bool:
        return False


# A Vertical move has a single string for the direction of the move
# The direction can be either "up" or "down"
class VerticalMove(Move):

    def __init__(self, direction: str):
        self.direction = direction

    def isVertical(self) -> bool:
        return True

    def isHorizontal(self) -> bool:
        return False

    def getTime(self) -> int:
        return 1

    def __str__(self) -> str:
        return f"{self.direction} Move"

    def __repr__(self):
        return self.__str__()


class PieceMove(Move):

    def __init__(self, type: str) -> None:
        self.type = type

    def isPlace(self) -> bool:
        return self.type == "place"

    def isPickup(self) -> bool:
        return self.type == "pickup"

    def isPiece(self) -> bool:
        return True

    def __str__(self) -> str:
        return f"{self.type} Move"

    def __repr__(self):
        return self.__str__()

    def getTime(self) -> int:
        return 0


class ResetMovement:
    # Takes in a list of movements
    def __init__(self, moves: List[Move]):
        self._moves: List[Move] = moves
        self._horizontalMoves = [m for m in moves if m.isHorizontal()]
        self._vertialMoves = [m for m in moves if m.isVertical()]

    def getStartingSquare(self):
        return self._horizontalMoves[0].start

    def getNumberOfVerticalMoves(self) -> int:
        # Calculates the number of vertical moves in the list
        return len(self._vertialMoves)

    def getNumberOfHorizontalMoves(self) -> int:
        return len(self._horizontalMoves)

    def getNumberOfMoves(self) -> int:
        return len(self._moves)

    def getTotalTime(self) -> int:
        return sum([m.getTime() for m in self._moves])

    def getTotalEuclidDistance(self) -> float:
        return sum(m.getEuclidDistance() for m in self._horizontalMoves)

    def getVerticalDistance(self) -> float:
        return VERTICAL_MOVEMENT_DISTANCE * self.getNumberOfVerticalMoves()

    def getFeatureArray(self, startingPosition) -> List[int]:
        # We want to compute a bunch of things about a movement in order to get a feature vector we can use to score each movement
        # Now in theory every single movement starts with a horizontal movement to the designated square and then ends with a vertical movement

        # So we have the currentPosition in x,y where 0,0 is the upper left of the bigger board

        # We have to find the first horizontal move and see where it happens

        return np.array([
            self._horizontalMoves[0].getEuclidDistance(),
            self.getNumberOfHorizontalMoves(),
            self.getNumberOfVerticalMoves(),
            self.getTotalEuclidDistance(),
            self.getTotalTime()
        ])
