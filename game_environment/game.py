from game_environment import board

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

    def run(self, get_move=None, *args):

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
                print("Invalid move")
                count += 1
            if count > 2:
                break

        score = max(self.curr_board.matrix)
        print("Score:", score)
        self.curr_board.print_matrix()
        print("Game Over")
        return score

