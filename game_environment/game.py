from game_environment import board
import pygame
from pygame.locals import *
import sys
import math
import time
import random

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
        valid = False
        is_over = False
        score = 0

        while not is_over:
            if(self.curr_board.is_full()):
                is_over = True
                continue

            MAX_MOVES = 0
            NUMBER_MAX = 1
            OUTPUT_RANKS = 2
            node_ranks = []
            max_nodes = []
            move = ""
            rank = 1

            
            #Copy the matrix to make a previous board with the newly spawned number
            self.previous_board.matrix = self.curr_board.make_copy_matrix()

            #Determine if the move is valid
            #Make this a separate thread to allow the program to run faster
            if get_move != None:
                #Get the move from the passed in function argument
                move_info = get_move(self, args[0])
                max_nodes = move_info[MAX_MOVES]
                #Get the ranks
                node_ranks = move_info[OUTPUT_RANKS]
            else:
                move = input("input move: ")
                node_ranks.append(node.Node(desc=move))

            #Get the highest ranked move. If mutliple pick a random one
            if len(max_nodes) > 0:
                index = random.randint(0, len(max_nodes) - 1)
                curr_node = max_nodes[index]
            #If there is no max move then no move was picked
            else:
                continue

            '''
            #-------Print Move Info------
            print(move_info[:-1])
            '''

            #Try out all the moves and determine the fitness based on the rank of the move
            for index in range(len(node_ranks)):
                prev_node = curr_node
                curr_node = node_ranks[index]
                #If the current nodes value is less than the previous then it is a lower rank move
                if curr_node.value != prev_node.value:
                    rank += 1

                #Get the description of the move from the node
                move = curr_node.desc

                #determine the move that was passed in and updates the board in memory
                self.curr_board.determine_move(move)

                #Determine if the resulting move did anything
                if(self.previous_board.matrix != self.curr_board.matrix):
                    #Determine the score made from the last round and update score
                    #Find the numbers on the board that arent 0
                    curr_pieces = [x for x in self.curr_board.matrix if x != 0]
                    prev_pieces = [x for x in self.previous_board.matrix if x != 0]
                    #Sort both so the tiles line up
                    curr_pieces.sort()
                    prev_pieces.sort()
                    #Determine the number of tiles combined
                    num_tiles_combined = len(prev_pieces) - len(curr_pieces)
                    #Get rid of tiles that are the same across both
                    #Whats left are the new tiles, add them up to get the score
                    for tile in prev_pieces:
                        if tile in curr_pieces:
                            curr_pieces.remove(tile)
                    score += sum(curr_pieces)
                    #Modify the score based on the move rank
                    score = score // rank

                    #Copy the matrix to make a previous board with the newly completed move
                    self.previous_board.matrix = self.curr_board.make_copy_matrix()
                    #Spawn a number
                    self.curr_board.spawn_number()
                    break
                '''
                #------------Print invalid move
                print("Invalid move")
                '''
        '''
        ---------------------------------------
        print("Score:", score)
        self.curr_board.print_matrix()
        print("Game Over")
        ---------------------------------------
        '''
        return score

class Game_Visual:
    def __init__(self, init_board=None):
        if init_board == None:
            init_board = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

        #Create the board
        self.curr_board = board.Board(init_board)
        self.previous_board = board.Board(init_board)

    def update_board(self, iteration, score, screen):
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
        screen.fill(BLACK)
        screen.blit(self.background_board, self.background_boardrect)

        #draw each piece to the screen
        for i in range(0, len(self.curr_board.matrix)):
            #Only draw a piece to the screen if it is non 0 in the matrix
            if self.curr_board.matrix[i] != 0:
                #Convert to base for coloring
                power_2 = math.log(self.curr_board.matrix[i], 2)
                #Draw the rectangle for the piece
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
                #Draw the number inside the rectangle
                text_surface = number_font.render(str(self.curr_board.matrix[i]), True, (255, 255, 255))
                screen.blit(text_surface, ((((i % 4) * SQ_WIDTH) + ((i % 4) * SEP_WIDTH)) + WHITE_SPACE_X + 45, 
                                        (((i // 4) * SQ_WIDTH) + ((i // 4) * SEP_WIDTH)) + WHITE_SPACE_Y + 30))

        title = title_font.render("Network: " + str(iteration), True, BLACK)
        title_width = title.get_rect().width
        screen.blit(title, (self.width // 2 - title_width / 2, 0))

        score_title = title_font.render("Score: " + str(score), True, BLACK)
        score_width = score_title.get_rect().width
        screen.blit(score_title, (self.width - (score_width + 10), 0))

        pygame.display.update()
        pygame.time.delay(50)
        

    def run(self, number=0, get_move=None, *args):
        #initialize classes
        pygame.init()

        #Window Size
        size = self.width, self.height = 548, 548

        #Set the screen size
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('2048-AI')

        #Get the background image from a picture
        self.background_board = pygame.image.load("background_board.png")
        #Create the object as a moving object
        self.background_boardrect = self.background_board.get_rect()

        #Spawn a number
        self.curr_board.spawn_number()
        score = 0
        is_over = False

        while not is_over:
            if(self.curr_board.is_full()):
                is_over = True
                continue
            #Copy the matrix to make a previous board with the newly spawned number
            self.previous_board.matrix = self.curr_board.make_copy_matrix()

            MAX_MOVES = 0
            NUMBER_MAX = 1
            OUTPUT_RANKS = 2
            node_ranks = []
            max_nodes = []
            move = ""
            rank = 1

            #Determine if the move is valid
            #Make this a separate thread to allow the program to run faster
            

            FINISH = float("inf")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and get_move == None:
                    if event.key == pygame.K_LEFT:
                        move = "left"
                        node_ranks.append(move)
                    elif event.key == pygame.K_RIGHT:
                        move = "right"
                        node_ranks.append(move)
                    elif event.key == pygame.K_DOWN:
                        move = "down"
                        node_ranks.append(move)
                    elif event.key == pygame.K_UP:
                        move = "up"
                        node_ranks.append(move)
                    else:
                        move = ""
            if get_move != None:
                #Get the move from the passed in function argument
                move_info = get_move(self, args[0])
                max_nodes = move_info[MAX_MOVES]
                #Get the ranks
                node_ranks = move_info[OUTPUT_RANKS]

            #Get the highest ranked move. If mutliple pick a random one
            if len(max_nodes) > 0:
                index = random.randint(0, len(max_nodes) - 1)
                curr_node = max_nodes[index]
            #If there is no max move then no move was picked
            else:
                continue    

            #Try out all the moves and determine the fitness based on the rank of the move
            for index in range(len(node_ranks)):
                prev_node = curr_node
                curr_node = node_ranks[index]
                #If the current nodes value is less than the previous then it is a lower rank move
                if curr_node.value != prev_node.value:
                    rank += 1

                #Get the description of the move from the node
                move = curr_node.desc

                #determine the move that was passed in and updates the board in memory
                self.curr_board.determine_move(move)
                
                #Determine if the resulting move did something
                if(self.previous_board.matrix != self.curr_board.matrix):
                    #Determine the score made from the current move and update score
                    #Find the numbers on the board that arent 0
                    curr_pieces = [x for x in self.curr_board.matrix if x != 0]
                    prev_pieces = [x for x in self.previous_board.matrix if x != 0]
                    #Sort both so the tiles line up
                    curr_pieces.sort()
                    prev_pieces.sort()
                    #Determine the number of tiles combined
                    num_tiles_combined = len(prev_pieces) - len(curr_pieces)
                    #Get rid of tiles that are the same across both
                    #Whats left in curr_pieces are the new tiles that were formed from the previous move
                    #add them up and add them with the current score to get the new score
                    for tile in prev_pieces:
                        if tile in curr_pieces:
                            curr_pieces.remove(tile)
                    score += sum(curr_pieces)
                    #adjust the score according to the rank of the move selected
                    score = score // rank
                    
                    #Copy the matrix to make a previous board with the newly completed move
                    self.previous_board.matrix = self.curr_board.make_copy_matrix()

                    #Print updated board to screen
                    self.update_board(number, score, screen)

                    for event in pygame.event.get():
                        pass

                    #Spawn a number
                    self.curr_board.spawn_number()

                    #Print updated board to screen
                    self.update_board(number, score, screen)

                    #-------Print Move Info------
                    print(move)  

                    break
                #If it doesnt do anything then try the other move
                '''
                #--------------Print invalid move----------------
                print("Invalid move"
                '''

        for event in pygame.event.get():
            pass
        pygame.time.delay(1500)
        return score
