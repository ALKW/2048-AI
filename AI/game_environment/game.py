import board
import pygame
from pygame.locals import *

class Game:
    def __init__(self):
        #Create the board
        self.board = board.Board()
        self.previous_board = board.Board()

    def run(self):
        #initialize classes
        pygame.init()

        #Create the board
        valid = False
        is_over = False

        #Spawn a number
        self.board.spawn_number()

        while not is_over:
            if(self.board.is_full()):
                is_over = True
                continue
            #Copy the matrix to make a previous board with the newly spawned number
            board.copy_length_16_matrix(self.board.matrix, self.previous_board.matrix)

            #Determine if the move is valid
            #Make this a separate thread to allow the program to run faster
            move = input("Move: ")
            if(move.lower() == 'e'):
                break
            if(move.lower() == "p"):
                board.print_matrix_4_rows(self.board.matrix)
                continue
            board.determine_move(move, self.board)
            #Determine if the resulting move did anything
            if(self.previous_board.matrix != self.board.matrix):
                #Copy the matrix to make a previous board with the newly completed move
                board.copy_length_16_matrix(self.board.matrix, self.previous_board.matrix)
                #Spawn a number
                self.board.spawn_number()

        print("Score:", max(self.board.matrix))    
        print("Game Over")

