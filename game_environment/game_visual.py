import sys
import pygame
from pygame.locals import *
import board
import math

def update_board(screen, board):
    SEP_WIDTH = 14
    SQ_WIDTH = 107
    WHITE_SPACE_X = 38
    WHITE_SPACE_Y = 37
    COLORS = ([255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0],
                [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],
                [0, 0, 255], [85, 0, 255], [170, 0, 255], [255, 0, 255],
                [255, 255, 255], [170, 170, 170], [85, 85, 85], [0, 0, 0],)
    screen.fill(BLACK)
    screen.blit(background_board, background_boardrect)

    for i in range(0, len(game_board.matrix)):
        if game_board.matrix[i] != 0:
            power_2 = math.log(game_board.matrix[i], 2)
            pygame.draw.rect(
                screen, 
                COLORS[int(power_2) % 15], 
                [ #Rectangle
                    (((i % 4) * SQ_WIDTH) + ((i % 4) * SEP_WIDTH)) + WHITE_SPACE_X, 
                    (((i // 4) * SQ_WIDTH) + ((i // 4) * SEP_WIDTH)) + WHITE_SPACE_Y, 
                    SQ_WIDTH, 
                    SQ_WIDTH
                ],#Rectangle Border
                0)
            textsurface = myfont.render(str(game_board.matrix[i]), True, (255, 255, 255))
            screen.blit(textsurface, ((((i % 4) * SQ_WIDTH) + ((i % 4) * SEP_WIDTH)) + WHITE_SPACE_X + 45, 
                                    (((i // 4) * SQ_WIDTH) + ((i // 4) * SEP_WIDTH)) + WHITE_SPACE_Y + 30))
    pygame.display.flip()

#initialize classes
pygame.init()

#Window Size
size = width, height = 548, 549

#Color
BLACK = 0, 0, 0
INIT_SQUARE_COLOR = 0, 0, 0
#Decrease order 0, 1, 2

#Set the screen size
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2048-AI')
pygame.display.set_icon(pygame.image.load("C:/Users/Alex/Documents/GitHub/2048-AI/game_environment/background_board.png"))

#Set the font
myfont = pygame.font.SysFont('Comic Sans MS', 30)

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
    if(game_board.is_full()):
        is_over = True
        continue
    #Copy the matrix to make a previous board with the newly spawned number
    board.copy_length_16_matrix(game_board.matrix, previous_board.matrix)

    #Determine if the move is valid
    #Make this a separate thread to allow the program to run faster
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
            board.determine_move(move, game_board)
            #Print board to screen 
            update_board(screen, game_board)

            #Determine if the resulting move did anything
            if(previous_board.matrix != game_board.matrix):
                #Copy the matrix to make a previous board with the newly completed move
                board.copy_length_16_matrix(game_board.matrix, previous_board.matrix)
                #Spawn a number
                game_board.spawn_number()
    #Print board to screen
    update_board(screen, game_board)

print("Score:", max(game_board.matrix))    
print("Game Over")
sys.exit()