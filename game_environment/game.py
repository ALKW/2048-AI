import board
import pygame
from pygame.locals import *

#initialize classes
pygame.init()

#Create the board
valid = False
is_over = False
game_board = board.Board()
previous_board = board.Board()

#Spawn a number
game_board.spawn_number()

while not is_over:
    if(game_board.is_full()):
        is_over = True
        continue
    #Copy the matrix to make a previous board with the newly spawned number
    board.copy_length_16_matrix(game_board.matrix, previous_board.matrix)

    #Determine if the move is valid
    #Make this a separate thread to allow the program to run faster
    move = input("Move: ")
    if(move == "E"):
        break
    board.determine_move(move, game_board)
    #Determine if the resulting move did anything
    if(previous_board.matrix != game_board.matrix):
        #Copy the matrix to make a previous board with the newly completed move
        board.copy_length_16_matrix(game_board.matrix, previous_board.matrix)
        #Spawn a number
        game_board.spawn_number()

print("Score:", max(game_board.matrix))    
print("Game Over")

