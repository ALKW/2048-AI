import pygame
from pygame.locals import *
import math
import sys

from Game_2048 import board

class Game_Visual():
    def __init__(self):
        #initialize classes
        pygame.init()

        #Window Size
        self.size = width, height = 548, 549

        #Set the screen size
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048-AI')


        #Get the background image from a picture
        self.background_board = pygame.image.load("background_board.png")
        #Create the object as a moving object
        self.background_boardrect = self.background_board.get_rect()

        #Create the board
        self.is_over = False
        self.game_board = board.Board()
        self.previous_board = board.Board()

    def update_board(self):
        BLACK = 0, 0, 0
        SEP_WIDTH = 14
        SQ_WIDTH = 107
        WHITE_SPACE_X = 38
        WHITE_SPACE_Y = 37
        COLORS = ([255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0],
                    [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],
                    [0, 0, 255], [85, 0, 255], [170, 0, 255], [255, 0, 255],
                    [255, 255, 255], [170, 170, 170], [85, 85, 85], [0, 0, 0],)
        #Set the font
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen.fill(BLACK)
        self.screen.blit(self.background_board, self.background_boardrect)

        #draw each piece to the screen
        for i in range(0, len(self.game_board.matrix)):
            if self.game_board.matrix[i] != 0:
                power_2 = math.log(self.game_board.matrix[i], 2)
                pygame.draw.rect(
                    self.screen, 
                    COLORS[int(power_2) % 15], 
                    [ #Rectangle
                        (((i % 4) * SQ_WIDTH) + ((i % 4) * SEP_WIDTH)) + WHITE_SPACE_X, 
                        (((i // 4) * SQ_WIDTH) + ((i // 4) * SEP_WIDTH)) + WHITE_SPACE_Y, 
                        SQ_WIDTH, 
                        SQ_WIDTH
                    ],#Rectangle Border
                    0)
                textsurface = myfont.render(str(self.game_board.matrix[i]), True, (255, 255, 255))
                self.screen.blit(textsurface, ((((i % 4) * SQ_WIDTH) + ((i % 4) * SEP_WIDTH)) + WHITE_SPACE_X + 45, 
                                        (((i // 4) * SQ_WIDTH) + ((i // 4) * SEP_WIDTH)) + WHITE_SPACE_Y + 30))
        pygame.display.flip()

    def run(self, get_move=None, *args):
        #Spawn a number
        self.game_board.spawn_number()
        count = 0

        while not self.is_over:
            if(self.game_board.is_full()):
                self.is_over = True
                continue
            #Copy the matrix to make a previous board with the newly spawned number
            self.previous_board.matrix = self.game_board.make_copy_matrix()

            move = ""

            #Determine if the move is valid
            #Make this a separate thread to allow the program to run faster
            if get_move == None:
                FINISH = float("inf")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            move = "left"
                        elif event.key == pygame.K_RIGHT:
                            move = "right"
                        elif event.key == pygame.K_DOWN:
                            move = "down"
                        elif event.key == pygame.K_UP:
                            move = "up"
                        else:
                            move = ""
            else:
                FINISH = 1
                move = get_move(args[0], args[1])
                if(move.lower() == 'e'):
                    break
                if(move.lower() == "p"):
                    self.game_board.print_matrix()
                    continue

            #determine the move that was passed in
            self.game_board.determine_move(move)
            #Print board to screen 
            self.update_board()

            #Determine if the resulting move did anything
            if(self.previous_board.matrix != self.game_board.matrix):
                #Copy the matrix to make a previous board with the newly completed move
                self.previous_board.matrix = self.game_board.make_copy_matrix()
                #Spawn a number
                self.game_board.spawn_number()
                count = 0
            else:
                #--------------print("Invalid move")----------------#
                count += 1
            if count > FINISH:
                break

        score = max(self.game_board.matrix)
        #Print board to screen
        self.update_board()

        sys.exit()
        return score