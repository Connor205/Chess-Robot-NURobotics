import os
from ThreadWithReturn import ThreadWithReturn

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from pygame.locals import *
from GameLogic import GameLogic
from BasicStockfishPlayers import BasicStockfishPlayers
import logging
from loggingConstants import formatter, handler
from Constants import *


class View:
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    states = [
        "WaitingForPlayer", "GettingPlayerMove", "ProcessingPlayerMove",
        "GettingComputerMove", "MakingComputerMove", "GameOver"
    ]
    revertStates = {
        'ProcessingPlayerMove': 'WaitingForPlayer',
    }

    def __init__(self, gl: GameLogic) -> None:
        self.logger.debug("Creating View")
        pg.init()
        self.logger.info("Initialized pygame")
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.defaultFont = pg.font.SysFont(None, 24)
        self.frame = 0
        # Possible States = 'WaitingForPlayer', 'GettingPlayerMove', 'ProcessingPlayerMove', 'GettingComputerMove', 'MakingComputerMove', 'GameOver'
        self.state = 'WaitingForPlayer'
        self.previousState = 'MakingComputerMove'
        self.gl = gl
        self.currentFen = gl.getCurretFenString()
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))

    def generateBoardFromFen(self, fenString):
        self.logger.debug("Generating board from fen: {}".format(fenString))
        self.board = pg.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.board.fill((255, 255, 255))
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                pg.draw.rect(self.board, color,
                             (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE,
                              SQUARE_SIZE))

        modifiedFen = fenString.replace(' ', '/', 1)
        ranks = modifiedFen.split('/')
        ranks = ranks[0:8]
        for rankI, rank in enumerate(ranks):
            file = 0
            index = 0
            while file < 8:
                char = rank[index]
                if char.isdigit():
                    file += int(char)
                else:
                    self.board.blit(PIECE_DICTIONARY[char]['image'],
                                    (file * SQUARE_SIZE, rankI * SQUARE_SIZE))
                    file += 1
                index += 1

    def isEventPlayerSwitch(self, event):
        return event.type == pg.KEYDOWN and event.key == pg.K_SPACE

    def gameLoop(self):
        self.logger.debug("Starting game loop")
        g = BasicStockfishPlayers()
        self.logger.info("Initialized GameLogic: {}".format(g.getLogicName()))
        self.screen.fill((255, 255, 255))
        running = True
        currentAwait = None
        previousResult = None
        currentState = 0
        newBoardRender = True
        while running:
            events = pg.event.get()
            # We want to manage the transition states differently than we do waiting states
            if not self.state == self.previousState:
                self.logger.debug("State changed from {} to {}".format(
                    self.previousState, self.state))
                if self.state == 'WaitingForPlayer':
                    # Nothing happens here, we dont kick off any concurrency
                    currentAwait = None
                if self.state == 'GettingPlayerMove':
                    currentAwait = ThreadWithReturn(self.gl.getPlayerMove)
                    currentAwait.start()
                if self.state == 'ProcessingPlayerMove':
                    currentAwait = ThreadWithReturn(self.gl.processPlayerMove,
                                                    previousResult)
                    currentAwait.start()
                if self.state == 'GettingComputerMove':
                    currentAwait = ThreadWithReturn(
                        self.gl.generateComputerMove)
                    currentAwait.start()
                if self.state == 'MakingComputerMove':
                    currentAwait = ThreadWithReturn(self.gl.makeComputerMove,
                                                    previousResult)
                    currentAwait.start()
                if self.state == 'GameOver':
                    currentAwait = None

                self.previousState = self.state
            else:
                if currentAwait is None:
                    currentState = currentState + 1
                    self.state = self.states[currentState % len(self.states)]
                elif not currentAwait.getActive():
                    previousResult = currentAwait.getResult()
                    if not previousResult:
                        if self.state in self.revertStates:
                            self.logger.error(
                                "Error in {}, restarting from {}".format(
                                    self.state, self.revertStates[self.state]))
                            self.state = self.revertStates[self.state]
                            currentState = self.states.index(self.state)
                        else:
                            self.logger.warning(
                                "Error in {}, restarting from beginning of state"
                                .format(self.state))
                            self.previousState = self.states[(currentState - 1)
                                                             %
                                                             len(self.states)]
                    else:
                        newFen = self.gl.getCurretFenString()
                        if not self.currentFen == newFen:
                            self.currentFen = newFen
                            newBoardRender = True
                        currentAwait = None
                        currentState = currentState + 1
                        self.state = self.states[currentState %
                                                 len(self.states)]

            if newBoardRender:
                self.generateBoardFromFen(self.currentFen)
                newBoardRender = False
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.board, (0, 0))
            self.screen.blit(
                self.defaultFont.render(f"Frame: {self.frame}", True,
                                        (0, 0, 0), (255, 255, 255)),
                (BOARD_WIDTH, 0))
            self.screen.blit(
                self.defaultFont.render(f"State: {self.state}", True,
                                        (0, 0, 0), (255, 255, 255)),
                (BOARD_WIDTH, 20))
            self.frame = self.frame + 1
            pg.display.flip()

            # loop through events to see if any of them are the escape key
            for event in events:
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                             and event.key == pg.K_ESCAPE):
                    running = False
