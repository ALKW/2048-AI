from game_environment import board
import sys
import pygame
from pygame.locals import *
import math
import time

class Game:
    def __init__(self, init_board=None):
        if init_board == None:
            init_board = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
            #Create the board and the previous board
            self.previous_board = board.Board(init_board)
            self.curr_board = board.Board(init_board)
            #Spawn a number if no board is passed through
            self.curr_board.spawn_number()
        else:
            #Create the board
            self.previous_board = board.Board(init_board)
            self.curr_board = board.Board(init_board)
            if init_board == [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]:
                #Spawn a number if the board is empty
                self.curr_board.spawn_number()

    def run(self, iteration=None, get_move=None, *args):

        #Create the board
        valid = False
        is_over = False
        count = 0

        while not is_over:
            if(self.curr_board.is_full()):
                is_over = True
                continue
            #Copy the matrix to make a previous board with the newly spawned number
            self.previous_board.matrix = self.curr_board.make_copy_matrix()

            #Determine if the move is valid
            #Make this a separate thread to allow the program to run faster
            if get_move == None:
                move = input("input move: ")
            else:
                move = get_move(args[0], args[1])

            if(move.lower() == 'e'):
                break
            if(move.lower() == "p"):
                self.curr_board.print_matrix()
                continue
            self.curr_board.determine_move(move)

            #Determine if the resulting move did anything
            if(self.previous_board.matrix != self.curr_board.matrix):
                #Copy the matrix to make a previous board with the newly completed move
                self.previous_board.matrix = self.curr_board.make_copy_matrix()
                #Spawn a number
                self.curr_board.spawn_number()
                count = 0
            else:
                #--------------print("Invalid move")----------------
                count += 1
            if count > 1:
                break

        score = max(self.curr_board.matrix)
        '''
        ---------------------------------------
        print("Score:", score)
        self.curr_board.print_matrix()
        print("Game Over")
        ---------------------------------------
        '''
        return score


class Game_Visual():
    def __init__(self, init_board=None):
        if init_board == None:
            init_board = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

        #initialize classes
        pygame.init()

        #Window Size
        self.size = self.width, self.height = 548, 548

        #Set the screen size
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048-AI')


        #Get the background image from a picture
        self.background_board = pygame.image.load("background_board.png")
        #Create the object as a moving object
        self.background_boardrect = self.background_board.get_rect()

        #Create the board
        self.is_over = False
        self.curr_board = board.Board(init_board)
        self.previous_board = board.Board(init_board)

    def update_board(self, iteration):
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
        number_font = pygame.font.SysFont('Comic Sans MS', 30)
        title_font = pygame.font.SysFont('Arial', 15)
        self.screen.fill(BLACK)
        self.screen.blit(self.background_board, self.background_boardrect)

        #draw each piece to the screen
        for i in range(0, len(self.curr_board.matrix)):
            #Only draw a piece to the screen if it is non 0 in the matrix
            if self.curr_board.matrix[i] != 0:
                #Convert to base for coloring
                power_2 = math.log(self.curr_board.matrix[i], 2)
                #Draw the rectangle for the piece
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
                #Draw the number inside the rectangle
                text_surface = number_font.render(str(self.curr_board.matrix[i]), True, (255, 255, 255))
                self.screen.blit(text_surface, ((((i % 4) * SQ_WIDTH) + ((i % 4) * SEP_WIDTH)) + WHITE_SPACE_X + 45, 
                                        (((i // 4) * SQ_WIDTH) + ((i // 4) * SEP_WIDTH)) + WHITE_SPACE_Y + 30))

        title = title_font.render("Network: " + str(iteration), True, BLACK)
        title_width = title.get_rect().width
        self.screen.blit(title, (self.width // 2 - title_width / 2, 0))

        pygame.display.flip()

    def run(self, number=0, get_move=None, *args):
        #Spawn a number
        self.curr_board.spawn_number()
        count = 0

        while not self.is_over:
            if(self.curr_board.is_full()):
                self.is_over = True
                continue
            #Copy the matrix to make a previous board with the newly spawned number
            self.previous_board.matrix = self.curr_board.make_copy_matrix()

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
                    self.curr_board.print_matrix()
                    continue

            #determine the move that was passed in
            self.curr_board.determine_move(move)
            #Print board to screen 
            self.update_board(number)

            #Determine if the resulting move did anything
            if(self.previous_board.matrix != self.curr_board.matrix):
                #Copy the matrix to make a previous board with the newly completed move
                self.previous_board.matrix = self.curr_board.make_copy_matrix()
                #Spawn a number
                self.curr_board.spawn_number()
                count = 0
            else:
                #--------------print("Invalid move")----------------#
                count += 1
            if count > FINISH:
                break

        score = max(self.curr_board.matrix)
        #Print board to screen
        self.update_board(number)

        return score
