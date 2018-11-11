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

