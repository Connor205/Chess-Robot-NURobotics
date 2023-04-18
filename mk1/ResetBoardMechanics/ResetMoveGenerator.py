from Board import Board
import numpy as np
import chess
from typing import Tuple, List
from ResetMoves import ResetMovement, HorizontalMove, VerticalMove, PieceMove
from pprint import pprint
from resetFinder import aStarSearch
# Lets go ahead and generate a goal board
TARGET_GOAL_BOARD = []

board = chess.Board()
for rank in range(8):
    row = ["", "", ""]
    for file in range(8):
        p = board.piece_at(chess.square(file, rank))
        if p is None:
            row.append("")
        else:
            row.append(p.symbol())
    row.append("")
    row.append("")
    row.append("")
    TARGET_GOAL_BOARD.append(row)

MAX_MM_PER_SECOND = 280
MIN_MM_PER_SECOND = 140
AVERAGE_MM_PER_SECOND = (MAX_MM_PER_SECOND + MIN_MM_PER_SECOND) / 2


def computeTimeToMove(d: float):
    return (d / 2) / MAX_MM_PER_SECOND + (d / 2) / MIN_MM_PER_SECOND


class PathFindingSearchProblem:

    def __init__(self, startingPos: Tuple[int, int], goalPos: Tuple[int, int],
                 board: np.ndarray):
        self.start = startingPos
        self.goal = goalPos
        self.board = board
        self._expanded = 0

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        # print("Checking Goal State of {}".format(state))
        return state == self.goal

    def getSuccessors(self, state):
        successors = []
        self._expanded += 1
        possibleActions = []
        x, y = state
        for i in range(1, 8):
            dx = i
            dy = 0
            nextx, nexty = int(x + dx), int(y + dy)
            if not (0 <= x + dx < len(
                    self.board[0])) or not self.board[nexty][nextx] == "":
                break
            possibleActions.append((dx, dy))
        for i in range(1, 8):
            dx = -i
            dy = 0
            nextx, nexty = int(x + dx), int(y + dy)
            if not (0 <= x + dx < len(
                    self.board[0])) or not self.board[nexty][nextx] == "":
                break
            possibleActions.append((dx, dy))
        for i in range(1, 8):
            dx = 0
            dy = i
            nextx, nexty = int(x + dx), int(y + dy)
            if not (0 <= y + dy < len(
                    self.board)) or not self.board[nexty][nextx] == "":
                break
            possibleActions.append((dx, dy))
        for i in range(1, 8):
            dx = 0
            dy = -i
            nextx, nexty = int(x + dx), int(y + dy)
            if not (0 <= y + dy < len(
                    self.board)) or not self.board[nexty][nextx] == "":
                break
            possibleActions.append((dx, dy))

        for action in possibleActions:
            x, y = state
            dx, dy = action
            nextx, nexty = int(x + dx), int(y + dy)
            if 0 <= nextx < len(self.board[0]) and 0 <= nexty < len(
                    self.board):
                if self.board[nexty][nextx] == "":
                    successors.append(
                        ((nextx, nexty), action,
                         computeTimeToMove(
                             (abs(nextx - x) + abs(nexty - y)) * 40)))
        return successors


def pathFindingSearchHeuristic(state, problem):
    return computeTimeToMove(((problem.goal[0] - state[0])**2 +
                              (problem.goal[1] - state[1])**2)**.5)


def generateResetMovesForSquare(
        s: Tuple[int, int], currentBoard: np.ndarray,
        currentPosition: Tuple[int, int]) -> List[ResetMovement]:
    # First we want to generate a list of all possible ending squares
    # This is done by iterating over the middle 8 by 8 rectangle and finding which squares have the same piece
    square_y, square_x = s
    piece_chr = currentBoard[square_y][square_x]

    # We can also do a check in the beginning to see if the piece is already in a valid position, this will save us some filtering
    if TARGET_GOAL_BOARD[square_y][square_x] == currentBoard[square_y][
            square_x] or piece_chr == "":
        return None

    validEndPositions = []
    for y in range(8):
        for x in range(3, 11):
            if TARGET_GOAL_BOARD[y][x] == piece_chr and currentBoard[y][
                    x] == "":
                validEndPositions.append((y, x))

    resetMovments = []
    # Find the best end position for the piece by finding the closest one to the starting position
    bestEndPosition = None
    bestDistance = 1000

    for p in validEndPositions:
        distance = abs(p[0] - square_y) + abs(p[1] - square_x)
        if distance < bestDistance:
            bestDistance = distance
            bestEndPosition = p

        if p is None:
            return None

        moves = []
        moves.append(HorizontalMove(currentPosition, s))
        moves.append(VerticalMove("down"))
        moves.append(PieceMove("pickup"))
        moves.append(VerticalMove("up"))
        moves.append(HorizontalMove(s, p))
        moves.append(VerticalMove("down"))
        moves.append(PieceMove("place"))
        moves.append(VerticalMove("up"))
        resetMovments.append(ResetMovement(moves))

        # Alright now we are going to write an A* algorithm to find the the shortest path between the two points in the grid
        # Lets use a* to find the shortest path between the two points
        # pprint(currentBoard)
        path = aStarSearch(
            PathFindingSearchProblem((s[1], s[0]), (p[1], p[0]), currentBoard),
            pathFindingSearchHeuristic)
        if path:
            # print("Found path")
            aMoves = []
            aMoves.append(HorizontalMove(currentPosition, s))
            aMoves.append(VerticalMove("down"))
            aMoves.append(PieceMove("pickup"))

            for i in range(len(path) - 1):
                aMoves.append(
                    HorizontalMove((path[i][1], path[i][0]),
                                   (path[i + 1][1], path[i + 1][0])))
            aMoves.append(PieceMove("place"))
            aMoves.append(VerticalMove("up"))
            resetMovments.append(ResetMovement(aMoves))

        # print(f"Generated: {len(resetMovments)} for square: {s}")

        return resetMovments


def generateAllResetMoves(currentPosition: Tuple[int, int], board: Board):
    # Alrighty so we need to generate a list of all valid movement sets in order to get the computer to evaluate each one
    # Each piece that could be reset is going to have 2 movements per ending square, the first is very simple its just:
    # Move to square, move down, move up, move to end square, move down, move up

    b = board.get_full_board()
    movements = []

    for y in range(8):
        for x in range(14):
            newMoves = generateResetMovesForSquare((y, x), b, currentPosition)
            if newMoves is not None:
                movements = movements + newMoves
    # print(len(movements))
    movements = [m for m in movements if m is not None]
    return movements


def evaluateListOfResetMoves(moves: List[ResetMovement]):
    return sum([m.getTotalTime() for m in moves])
