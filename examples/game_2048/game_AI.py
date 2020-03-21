"""The Game 2048 that is played by the AI. Uses the board class as an object for data storage"""

import sys
import math
import os

import pygame
import pygame.locals

from game_2048 import board

class Game:
    '''
    The game object for 2048 that operates in a game loop. There are no visuals, this is pure
    backend

    Constructor Args:
        init_board - (list) - The optional initial board for the game
    Raises:
        None
    '''
    EMPTY_BOARD = [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0
        ]
    MAX_MOVES = 0
    OUTPUT_RANKS = 2
    BLACK = 0, 0, 0
    SEP_WIDTH = 14
    SQ_WIDTH = 107
    WHITE_SPACE_X = 38
    WHITE_SPACE_Y = 37
    COLORS = ([255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0],
              [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],
              [0, 0, 255], [85, 0, 255], [170, 0, 255], [255, 0, 255],
              [255, 255, 255], [170, 170, 170], [85, 85, 85], [0, 0, 0],)

    def __init__(self, init_board=None):
        if init_board is None:
            init_board = Game.EMPTY_BOARD

        # Create the board and the previous board
        self.prev_board = board.Board(init_board)
        self.curr_board = board.Board(init_board)

        # Spawn a number if the board is empty
        if init_board == Game.EMPTY_BOARD:
            self.curr_board.spawn_number()

        self.score = 0

    def run(self, individual, get_move):
        '''
        Runs the game in a game loop. This is independent of the neural network and does no
        processing. It only runs the game and reports the score

        Args:
            get_move - (function) - user defined function that determines what move the board
            should do
        Returns:
            (int) - the fitness (performance) of the network after the game is over
        Raises:
            exception_name
        '''
        is_over = False
        self.score = 0

        # Loop until we lose
        while not is_over:
            if self.curr_board.is_full():
                is_over = True
                continue

            # Do the move and if its a valid move, spawn a number
            move = get_move(self, individual)
            if (self.curr_board.exec_move(move) and
                    self.prev_board.matrix != self.curr_board.matrix):
                # If the move was valid update the score and spawn another number
                self.update_score()
                self.curr_board.spawn_number()
                self.prev_board.matrix = self.curr_board.make_copy_matrix()

        return self.score

    def update_score(self):
        '''
        Determines the score of the move. Combining two tiles with values x yields an additional
        2 * x in score. Adds this to the current score for the object

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        curr_pieces = [x for x in self.curr_board.matrix if x != 0]
        prev_pieces = [x for x in self.prev_board.matrix if x != 0]

        curr_pieces.sort()
        prev_pieces.sort()

        # Get rid of tiles that are the same across both
        # Whats left are the new tiles, add them up to get the additonal score
        for tile in prev_pieces:
            if tile in curr_pieces:
                curr_pieces.remove(tile)

        self.score += sum(curr_pieces)

class GameVisual(Game):
    '''
    The game object for 2048 that operates in a game loop. Includes visuals and draws user defined 
    items as well

    Constructor Args:
        init_board - (list) - The optional initial board for the game
    Raises:
        None
    '''
    def __init__(self, init_board=None):
        super().__init__(init_board)

        # Set the background of the game
        self.background_board = pygame.image.load(os.path.join(os.getcwd(), "examples", "game_2048", 
                                                               "background_board.png"))
        self.background_boardrect = self.background_board.get_rect()

        # Set the width and height of the screen
        self.width = 548
        self.height = 548
        self.size = self.width, self.height

    def run_vis(self, individual, get_move, draw_extra):
        '''
        Runs the game in a game loop. This is independent of the neural network and does no
        processing. It only runs the game and reports the score. It over rides the parent class Game
        and adds graphics while running.

        Args:
            get_move - (function) - user defined function that determines what move the board
            should do
        Returns:
            (int) - the fitness (performance) of the network after the game is over
        Raises:
            exception_name
        '''
        # initialize classes
        pygame.init()

        # Set the screen size
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048-AI')

        is_over = False
        self.score = 0

        # Loop until we lose
        while not is_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.curr_board.is_full():
                is_over = True
                continue

            # Do the move and if its a valid move, spawn a number
            move = get_move(self, individual)
            if (self.curr_board.exec_move(move) and
                    self.prev_board.matrix != self.curr_board.matrix):
                # Print updated board to screen
                self.update_board(screen, draw_extra, individual)

                # If the move was valid update the score and spawn another number
                self.update_score()

                # Used to update screen
                for event in pygame.event.get():
                    pass

                # Spawn a number
                self.curr_board.spawn_number()

                # Print updated board to screen
                self.update_board(screen, draw_extra, individual)

        return self.score

    def update_board(self, screen, draw_extra, individual):
        '''
        Updates the screen after each move of the board
        
        Args:
            screen - (pygame.screen) - The screen object pygame uses to draw on
            draw_extra - (function) - extra user defined function that draws additional
                                      objects to the screen object
            individual - (Network) - network object that contains data to draw to the screen
        Returns:
            None
        Raises:
            None
        '''
        # Set the font
        number_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_font = pygame.font.SysFont('Arial', 15)
        screen.fill(Game.BLACK)
        screen.blit(self.background_board, self.background_boardrect)

        # draw each piece to the screen
        for i in range(0, len(self.curr_board.matrix)):
            # Only draw a piece to the screen if it is non 0 in the matrix
            if self.curr_board.matrix[i] != 0:
                # Convert to base for coloring
                power_2 = math.log(self.curr_board.matrix[i], 2)

                rect_x = ((((i % 4) * Game.SQ_WIDTH) + ((i % 4) * Game.SEP_WIDTH))
                          + Game.WHITE_SPACE_X)
                rect_y = ((((i // 4) * Game.SQ_WIDTH) + ((i // 4) * Game.SEP_WIDTH))
                          + Game.WHITE_SPACE_Y)

                # Draw the rectangle for the piece
                pygame.draw.rect(
                    screen, # Screen to draw to
                    Game.COLORS[int(power_2) % 15], # background Color to be used
                    [rect_x, rect_y, Game.SQ_WIDTH, Game.SQ_WIDTH], # Rectangle
                    0 # Rectangle Border
                    )

                # Draw the number inside the rectangle
                number = number_font.render(str(self.curr_board.matrix[i]), True, (255, 255, 255))
                single_number_width = number_font.render(str(1), True, (255, 255, 255))\
                                                 .get_rect()\
                                                 .width
                number_width = number.get_rect().width
                num_x = (
                    (((i % 4) * Game.SQ_WIDTH)
                     + ((i % 4) * Game.SEP_WIDTH))
                    + Game.WHITE_SPACE_X + 45
                    ) - number_width // 2 + single_number_width / 2
                num_y = ((((i // 4) * Game.SQ_WIDTH) + ((i // 4) * Game.SEP_WIDTH))
                         + Game.WHITE_SPACE_Y + 30)
                screen.blit(number, (num_x, num_y))

        self.draw_score(text_font, screen)

        draw_extra(self, screen, individual)

        pygame.display.update()
        pygame.time.delay(50)

    def draw_score(self, text_font, screen):
        '''
        Draws the score to the screen
        
        Args:
            textfont - (pygame.font) - The font for the text to be drawn to the screen
        Returns:
            None
        Raises:
            None
        '''
        score_title = text_font.render("Score: " + str(self.score), True, Game.BLACK)
        screen.blit(score_title, (10, 0))