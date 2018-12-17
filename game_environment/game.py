from game_environment import board

class Game:
    def __init__(self):
        #Create the board
        self.board = board.Board()
        self.previous_board = board.Board()

    def run(self, get_move=0):

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
            self.previous_board.matrix = self.board.copy_matrix(self.previous_board.matrix)

            #Determine if the move is valid
            #Make this a separate thread to allow the program to run faster
            if get_move == 0:
                move = input("input move: ")
            else:
                move = get_move()
            if(move.lower() == 'e'):
                break
            if(move.lower() == "p"):
                self.board.print_matrix()
                continue
            self.board.determine_move(move)
            #Determine if the resulting move did anything
            if(self.previous_board.matrix != self.board.matrix):
                #Copy the matrix to make a previous board with the newly completed move
                self.previous_board.matrix = self.board.copy_matrix(self.previous_board.matrix)
                #Spawn a number
                self.board.spawn_number()
                print("Invalid move")

        print("Score:", max(self.board.matrix))    
        print("Game Over")

