from math import sqrt
import chess
import heapq


class WeightedNode:
    state = None
    path = None
    cost = None

    def __init__(self, state, path, cost) -> None:
        self.state = state
        self.path = path
        self.cost = cost

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, WeightedNode) and self.state == __o.state


init_board = chess.Board()


class ResetSearchProblem:

    def __init__(self, startingGameState):
        self.start = startingGameState
        self._expanded = 0

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        print("Checking Goal State of {}".format(state))
        return state[0].split(" ")[0] == init_board.fen().split(" ")[0]

    def getSuccessors(self, state):
        successors = []
        self._expanded += 1
        b: chess.Board = chess.Board(state[0])
        white = state[1]
        black = state[2]
        empty_squares = [x for x in chess.SQUARES if b.piece_at(x) is None]
        print("Empty Squares: {}".format(empty_squares))
        for i in range(64):
            p = b.piece_at(i)

            if p is not None and init_board.piece_at(i) != p:
                min_dist = 100
                min_square = None
                for j in empty_squares:
                    if init_board.piece_at(j) == p:
                        d = chess.square_distance(i, j)
                        if d <= min_dist:
                            min_dist = d
                            min_square = j
                if min_square is not None:
                    new_board = b.copy()
                    new_board.set_piece_at(min_square, p)
                    new_board.remove_piece_at(i)
                    successors.append(((new_board.fen(), white, black), (i, j),
                                       chess.square_distance(i, j)))
        return successors


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(),
                      startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {
        }  # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1  # DO NOT CHANGE
        for direction in [
                Directions.NORTH, Directions.SOUTH, Directions.EAST,
                Directions.WEST
        ]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def resetHueristic(state, problem=None):
    count = 0
    b = chess.Board(state[0])
    for i in range(64):
        if b.piece_at(i) != init_board.piece_at(i):
            count += 1
    return count


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    ss = problem.getStartState()
    starting_node = WeightedNode(ss, [ss], 0)
    frontier = PriorityQueue()
    frontier.push(starting_node, heuristic(ss, problem))
    explored = set()
    while True:
        if frontier.isEmpty():
            return False
        current_node = frontier.pop()
        explored.add(current_node.state)
        if problem.isGoalState(current_node.state):
            return current_node.path
        for successor in problem.getSuccessors(current_node.state):
            step_cost = successor[2]
            next_cost = current_node.cost + step_cost
            next_priority = next_cost + heuristic(successor[0], problem)
            next_node = WeightedNode(successor[0],
                                     current_node.path + [successor[0]],
                                     next_cost)
            if successor[0] not in explored:
                frontier.update(next_node, next_priority)


def findPath(fen, captured):
    white = 1
    black = 1
    return aStarSearch(ResetSearchProblem((fen, white, black)), resetHueristic)


whiteSetup = [
    list("RNBQQBNR"),
    list("PPPPPPPP"),
]
blackSetup = [
    ["r", "p"],
    ["n", "p"],
    ["b", "p"],
    ["q", "p"],
    ["q", "p"],
    ["b", "p"],
    ["n", "p"],
    ["r", "p"],
]


def calculateMoveDistance(m):
    if m[0] == "board":
        return chess.square_distance(m[1], m[2])
    if m[0] == "white":
        return 2 - m[2] + chess.square_distance(chess.square(m[1], 7), m[3])
    if m[0] == "black":
        if m[1] == -1:
            return 1 + chess.square_distance(chess.square(0, m[2]), m[3])
        else:
            return 1 + chess.square_distance(chess.square(7, m[2]), m[3])


def getSuccessors(fen, white, black):
    successors = []
    b: chess.Board = chess.Board(fen)
    empty_squares = [x for x in chess.SQUARES if b.piece_at(x) is None]
    for i in range(64):
        p = b.piece_at(i)
        if p is not None and init_board.piece_at(i) != p:
            min_dist = 100
            min_square = None
            for j in empty_squares:
                if init_board.piece_at(j) == p:
                    d = sqrt((chess.square_file(i) - chess.square_file(j))**2 +
                             (chess.square_rank(i) - chess.square_rank(j))**2)
                    if d <= min_dist:
                        min_dist = d
                        min_square = j
            if min_square is not None:
                new_board = b.copy()
                new_board.set_piece_at(min_square, p)
                new_board.remove_piece_at(i)
                successors.append(((new_board.fen(), white, black),
                                   ("board", i, min_square), min_dist))
    # White takens
    for x in range(8):
        for y in range(2):
            min_dist = 100
            min_square = None
            if x == 3 and y == 0:
                continue
            if white[y, x] == 1:
                p = whiteSetup[y][x]
                for e in empty_squares:
                    if str(init_board.piece_at(e)) == p:
                        d = calculateMoveDistance(("white", x, y, e))
                        if d <= min_dist:
                            min_dist = d
                            min_square = e
            if min_square is not None:
                new_board = b.copy()
                new_board.set_piece_at(min_square,
                                       init_board.piece_at(min_square))
                newWhite = white.copy()
                newWhite[y, x] = 0
                successors.append(((new_board.fen(), newWhite, black),
                                   ("white", x, y, min_square), min_dist))
    # Black takens
    for x in [-1, 1]:
        for y in range(8):
            min_dist = 100
            min_square = None
            if x == -1 and y == 3:
                continue
            if x == -1:
                blackCoord = 0
            else:
                blackCoord = 1
            if black[y, blackCoord] == 1:
                p = blackSetup[y][blackCoord]
                for e in empty_squares:
                    # print(e, init_board.piece_at(e))
                    if str(init_board.piece_at(e)) == p:
                        d = calculateMoveDistance(("black", x, y, e))
                        if d <= min_dist:
                            min_dist = d
                            min_square = e
            if min_square is not None:
                new_board = b.copy()
                new_board.set_piece_at(min_square,
                                       init_board.piece_at(min_square))
                newBlack = black.copy()
                newBlack[y, x] = 0
                successors.append(((new_board.fen(), white, newBlack),
                                   ("black", x, y, min_square), min_dist))

    return successors


startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


def findPathGreedy(fen, captured):
    currentSquare = 56
    currentFen = fen
    w = captured.white
    b = captured.black
    moves = []
    while (currentFen.split(" ")[0] != startingFen):
        print("Fen: " + currentFen)
        print("White: " + str(w))
        print("Black: " + str(b))
        possibleMoves = getSuccessors(currentFen, w, b)
        bestCost = 100
        if len(possibleMoves) == 0:
            return False
        for m in possibleMoves:
            if m[1][0] == "board":
                dstToStart = chess.square_distance(m[1][1], currentSquare)
            if m[1][0] == "white":
                dstToStart = calculateMoveDistance(
                    ("white", m[1][1], m[1][2], m[1][3]))
            if m[1][0] == "black":
                dstToStart = calculateMoveDistance(
                    ("black", m[1][1], m[1][2], m[1][3]))
            cost = m[2] + dstToStart
            if cost < bestCost:
                bestCost = cost
                bestMove = m

        currentSquare = bestMove[1][-1]
        currentFen = bestMove[0][0]
        w = bestMove[0][1]
        b = bestMove[0][2]
        moves.append((bestMove[1], bestMove[0][0]))
        print(bestMove[1])
    return moves


def convertSquareToCoordinates(square: str):
    return [ord(square[0]) - ord('a'), 8 - int(square[1])]


def getAdjacentSquares(square: int):
    return [square + 1, square - 1, square + 8, square - 8]


def isMoveLift(fen, move):
    b = chess.Board(fen)
    if move[0] == "board":
        # Check to see if there are pieces between start and end square

        start = move[1]
        end = move[2]
        minimum = min(start, end)
        maximum = max(start, end)
        offset = maximum - minimum
        if offset % 8 == 0:
            for i in range(minimum + 8, maximum, 8):
                if b.piece_at(i) is not None:
                    return False
        if chess.square_file(start) == chess.square_file(end):
            for i in range(minimum + 1, maximum):
                if b.piece_at(i) is not None:
                    return False
        if offset % 9 == 0:
            for i in range(minimum + 9, maximum, 9):
                if b.piece_at(i) is not None:
                    return False
                for s in getAdjacentSquares(i):
                    if b.piece_at(s) is not None:
                        return False
        if offset % 7 == 0:
            for i in range(minimum + 7, maximum, 7):
                if b.piece_at(i) is not None:
                    return False
                for s in getAdjacentSquares(i):
                    if b.piece_at(s) is not None:
                        return False
    return True


# def reset_game_board(fen, captured: CapturedPieceManagement):
#     a = Arduino.Arduino("/dev/cu.usbmodem142101")
#     a.waitForReady()
#     path = findPathGreedy(fen, captured)
#     if path is False:
#         print("Unable to find path")
#         return False
#     for m, f in path:
#         if m[0] == "board":
#             startSquare = convertSquareToCoordinates(chess.square_name(m[1]))
#             endSquare = convertSquareToCoordinates(chess.square_name(m[2]))
#             a.sendCommand("move", [startSquare[0], startSquare[1]])
#             a.waitForReady()
#             if isMoveLift(f, m):
#                 a.sendCommand("pickup", [])
#             else:
#                 a.sendCommand("smallPickup", [])
#             a.waitForReady()
#             a.sendCommand("move", [endSquare[0], endSquare[1]])
#             a.waitForReady()
#             a.sendCommand("drop", [])
#             a.waitForReady()
#         if m[0] == "white":
#             a.sendCommand("moveWhiteTaken", [m[1], m[2]])
#             a.waitForReady()
#             a.sendCommand("pickupTaken", [])
#             endSquare = convertSquareToCoordinates(chess.square_name(m[3]))
#             a.sendCommand("move", [endSquare[0], endSquare[1]])
#             a.waitForReady()
#             a.sendCommand("drop", [])
#             a.waitForReady()
#         if m[0] == "black":
#             a.sendCommand("moveBlackTaken", [m[1], m[2]])
#             a.waitForReady()
#             a.sendCommand("pickupTaken", [])
#             endSquare = convertSquareToCoordinates(chess.square_name(m[3]))
#             a.sendCommand("move", [endSquare[0], endSquare[1]])
#             a.waitForReady()
#             a.sendCommand("drop", [])
#             a.waitForReady()

if __name__ == "__main__":
    # cap = CapturedPieceManagement()
    b = chess.Board()
    # b.push_uci("e2e4")
    # b.push_uci("e7e5")
    # b.push_uci("g1f3")
    # b.push_uci("b8c6")
    # b.push_uci("f3e5")
    # cap.placePiece("black", "pawn")
    # b.push_uci("c6e5")
    # cap.placePiece("white", "knight")
    # b.push_uci("d1g4")
    # b.push_uci("f7f5")
    # b.push_uci("f4d5")
    # b.push_uci("c7c6")
    # b.push_uci("e1g1")
    # b.push_uci("c6b5")
    # cap.placePiece("white", "bishop")
    # b.push_uci("e4f5")
    # cap.placePiece("black", "pawn")
    # b.push_uci("e5g4")
    # cap.placePiece("white", "queen")
    # b.push_uci("d2d3")
    # b.push_uci("f8a3")
    # b.push_uci("b2a3")
    # cap.placePiece("black", "bishop")
    # b.push_uci("g4f2")
    # cap.placePiece("white", "pawn")
    # b.push_uci("f1f2")
    # cap.placePiece("black", "knight")
    # b.push_uci("d8g5")
    # b.push_uci("c1f4")
    # b.push_uci("d7d5")
    # b.push_uci("b1c3")
    # b.push_uci("g8f6")

    # b.set_board_fen("r3k1nr/p4pNp/n7/1p1pP2P/6P1/3P1Q2/PRP1K3/q5bR")
    # cap.placePiece("black", "pawn")
    # cap.placePiece("black", "pawn")
    # cap.placePiece("black", "pawn")
    # cap.placePiece("black", "bishop")
    # cap.placePiece("white", "pawn")
    # cap.placePiece("white", "pawn")
    # cap.placePiece("white", "bishop")
    # cap.placePiece("white", "bishop")
    # cap.placePiece("white", "knight")
    # print(findPathGreedy(b.fen(), cap))
    # reset_game_board(b.fen(), cap)
