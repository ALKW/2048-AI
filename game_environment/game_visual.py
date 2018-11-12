import sys
import pygame
from pygame.locals import *
import board

pygame.init()

#Window Size
size = width, height = 548, 549

#Color
BLACK = 0, 0, 0
INIT_SQUARE_COLOR = 0, 0, 0
#Decrease order 0, 1, 2

#Set the screen size
screen = pygame.display.set_mode(size)

#Get the background image from a picture
background_board = pygame.image.load("C:/Users/Alex/Documents/GitHub/2048-AI/game_environment/background_board.png")
#Create the object as a moving object
background_boardrect = background_board.get_rect()

#Create the board
valid = False
is_over = False
game_board = board.Board()
previous_board = board.Board()

#Spawn a number
game_board.spawn_number()

while not is_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if(game_board.is_full()):
        is_over = True
        continue
    #Print out the board in the console
    board.print_matrix_4_rows(game_board.matrix)
    #Copy the matrix to make a previous board with the newly spawned number
    board.copy_length_16_matrix(game_board.matrix, previous_board.matrix)

    #Determine if the move is valid
    #Make this a separate thread to allow the program to run faster
    move = input("Input Movement: ")
    valid = board.determine_move(move, game_board)

    #Determine if the resulting move did anything
    if(previous_board.matrix != game_board.matrix):
        #Print the result of the move        
        board.print_matrix_4_rows(game_board.matrix)
        print("Completed Move")
        #Copy the matrix to make a previous board with the newly completed move
        board.copy_length_16_matrix(game_board.matrix, previous_board.matrix)
        #Spawn a number
        game_board.spawn_number()
    else:
        board.print_matrix_4_rows(game_board.matrix)
        print("invalid move")

    screen.fill(BLACK)
    screen.blit(background_board, background_boardrect)

    x, y = 1, 1
    for i in range(0, len(game_board.matrix)):
        if game_board.matrix[i] != 0:
            pygame.draw.rect(screen, INIT_SQUARE_COLOR, [x + (((i % 4) * 107) + ((i % 4) * 14)) + 37, y + (((i // 4) * 107) + ((i // 4) * 14)) + 37, 107, 107], 0)
    pygame.display.flip()

print("Game Over")
sys.exit()