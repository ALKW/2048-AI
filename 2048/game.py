import board

def determine_move(move, board):
    '''
    Executes move based on user input, move must match and of the
    strings below otherwise invalid move is printed
    
    Args: 
        move (Str) valid options: "up", "left", "right", "down"
        board (Board Object)
    Returns:
        Boolean - true if move is matches any provided move, false if
        move does not match any provided move
    Raises: 
        None
    '''
    if(move == "up"):
        board.up_movement()
        return True
    elif(move == "down"):
        board.down_movement()
        return True
    elif(move == "left"):
        board.left_movement()
        return True
    elif(move == "right"):
        board.right_movement()
        return True
    else:
        print("invalid move*")
        return False

def copy_length_16_matrix(matrix, new_matrix):
    '''
    Copies array of length 16 into another array of length 16
    
    Args: 
        matrix (list of length 16) matrix to copy from
        new_matrix (list of length 16) matrix to be copied to
    Returns:
        new_matrix
    Raises: 
        None
    '''
    for i in range(0, 16):
        new_matrix[i] = matrix[i]
    return new_matrix

valid = False
is_over = False
game_board = board.Board()
previous_board = board.Board()

while(not is_over):
    if(game_board.is_full()):
        is_over = True
        continue
    game_board.spawn_number()
    board.print_matrix_4_rows(game_board.matrix)
    copy_length_16_matrix(game_board.matrix, previous_board.matrix)
    while(not valid):
        move = input("Input Movement: ")
        valid = determine_move(move, game_board)
        if(previous_board.matrix == game_board.matrix):
            print("invalid move")
            valid = False
    board.print_matrix_4_rows(game_board.matrix)
    print("Completed Move")
    copy_length_16_matrix(game_board.matrix, previous_board.matrix)
    valid = False

print("Game Over")

