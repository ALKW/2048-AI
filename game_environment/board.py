import random

class Matrix:
    row_one = slice(0, 4)
    row_two = slice(4, 8)
    row_three = slice(8, 12)
    row_four = slice(12, 16)
    rows = [row_one, row_two, row_three, row_four]

    column_one = slice(0, 16, 4)
    column_two = slice(1, 16, 4)
    column_three = slice(2, 16, 4)
    column_four = slice(3, 16, 4)
    columns = [column_one, column_two, column_three, column_four]

class Board(Matrix):
    score = 0

    def __init__(self, board):
        self.matrix = board

    def choose(self):
        '''
        Chooses 4 with probablility 0.2 and 2 with probability 0.8

        Args:
            None
        Returns:
            (int) - 20% of the time: 4
                    80% of the time: 2
        Raises:
            None
        '''
        probability = random.randrange(1, 11)
        if(probability >= 2):
            return 2
        else:
            return 4

    def pick_position(self):
        '''
        Picks a random number between 0 and 15
        
        Args:
            None
        Returns:
            (int) - random between 0 and 15
        Raises:
            None
        '''
        p = random.randint(0, 15)
        return p
    
    def spawn_number(self):
        '''
        Creates either a 4 or a 2 anywhere a zero is in the objects list

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        number_to_insert = self.choose()
        position = random.randint(0, 15)
        while(self.matrix[position] != 0):
            if(self.is_full()):
                break
            position = self.pick_position()
        self.matrix[position] = number_to_insert
    
    def is_full(self):
        '''
        Determines if a list contains any zeros and returns true if it 
        doesn't and false if it does

        Args:
            None
        Returns:
            (Boolean) - True if list doesnt contain: 0
                        False if list contains: 0
        Raises:
            None
        '''
        if (min(self.matrix) == 0):
            return False
        else:
            return True
    
    def remove_from_list(self, this_list, value):
        '''
        Removes all 0's from a list and does not replace them

        Args:
            this_list (list) - List of any length
            value (int) - value to be removed
        Returns:
            (list) - this_list with values removed
        Raises:
            None
        '''
        return [value for value in this_list if value != 0]
    
    def fill_in_zeros(self, this_list, value, length):
        '''
        Appends values to the end of a list up to a specified length

        Args:
            this_list (list) - list to be modified
            value (int) - value to be appeneded to end of list
            length (int) - length of list
        Returns:
            (list) - this_list with values appended
        Raises:
            None
        '''
        while(len(this_list) != length):
            this_list.append(value)
        return this_list

    def up_movement(self):
        '''
        Performs an up movement on the matrix within the board object.
        The movement will go through all columns in the matrix. The 
        matrix is a list of length 16 and is arranged in a 4x4 grid with
        position 0 in the top left and the list extending right and
        ending with position 16 in the bottom right. For each column the
        slice associated with has its 0's removed and not replaced. The
        column is then appended with 0's until the length is 4. Starting
        at the top of the column, if the number below is the same then
        the numbers are combined and the result is copied to a new array
        with the number below being deleted if not then the number is 
        copied without modification. 0's are ignored.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for i in range(0, 4):
            curr_column = self.matrix[self.columns[i]]
            curr_column = self.remove_from_list(curr_column, 0)
            curr_column = self.fill_in_zeros(curr_column, 0, 4)
            new_values = [0, 0, 0, 0]
            counter = 0
            need_to_skip = False
            #clears out 0s in the column
            #checks for numbers that are the same that are next to each other
            for k in range(0, 4):
                #skips iteration in for loop.
                if(need_to_skip):
                    need_to_skip = False
                    continue
                #0s are at the end, if hit then we are done with column
                elif(curr_column[k] == 0):
                    continue
                #checks to see if the numbers are the same in columns and combines them if they are the same. Sets flag to skip next number
                elif(k < 3 and curr_column[k] == curr_column[k + 1]):
                    value = curr_column[k] * 2
                    curr_column[k] = 0
                    curr_column[k + 1] = 0
                    new_values[counter] = value
                    counter += 1
                    need_to_skip = True
                #number is unique so it is added without modification to the new values column
                else:
                    new_values[counter] = curr_column[k]
                    counter += 1
            #assigns the new values to the board
            self.matrix[self.columns[i]] = new_values
    
    def down_movement(self):
        '''
        Performs a down movement, similar to the game 2048,
        on the matrix within the board object. The movement will go 
        through all columns in the matrix. The matrix is a list of 
        length 16 and is arranged in a 4x4 grid with position 0 in the 
        top left and the list extending right and ending with position 16
        in the bottom right. For each column, the slice associated 
        with has its 0's removed and not replaced. The column is then 
        appended with 0's until the length is 4. The column is then 
        reversed. Starting at the top of the column, if the  number 
        below is the same then the numbers are combined and the result 
        is copied to a new array with the number below being deleted if
        not then the number is copied without modification. 0's are ignored.
        The move is an up move with the column reversed.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for i in range(0, 4):
            curr_column = self.matrix[self.columns[i]]
            #reverses and clears out 0s in the column, uses temp column to allow loop to execute correctly, otherwise 2 zeros in first positions creates problem
            curr_column.reverse()
            curr_column = self.remove_from_list(curr_column, 0)
            curr_column = self.fill_in_zeros(curr_column, 0, 4)
            new_values = [0, 0, 0, 0]
            counter = 0
            need_to_skip = False
            #checks for numbers that are the same that are next to each other
            for k in range(0, 4):
                #skips iteration in for loop.
                if(need_to_skip):
                    need_to_skip = False
                    continue
                #0s are at the end, if hit then we are done with column
                elif(curr_column[k] == 0):
                    continue
                #checks to see if the numbers are the same in columns and combines them if they are the same. Sets flag to skip next number
                elif(k < 3 and curr_column[k] == curr_column[k + 1]):
                    value = curr_column[k] * 2
                    curr_column[k] = 0
                    curr_column[k + 1] = 0
                    new_values[counter] = value
                    counter += 1
                    need_to_skip = True
                #number is unique so it is added without modification to the new values column
                else:
                    new_values[counter] = curr_column[k]
                    counter += 1
            #assigns the new values to the board
            new_values.reverse()
            self.matrix[self.columns[i]] = new_values

    def left_movement(self):
        '''
        Performs a left movement, similar to the game 2048,
        on the matrix within the board object. The movement will go 
        through all rows in the matrix. The matrix is a list of 
        length 16 and is arranged in a 4x4 grid with position 0 in the 
        top left and the list extending right and ending with position 16
        in the bottom right. For each row, the slice associated 
        with has its 0's removed and not replaced. The row is then 
        appended with 0's until the length is 4. Starting at the far 
        right of the row, if the number to the left is the same then 
        the numbers are combined and the result is copied to a new 
        array with the number below being deleted if not then the number
        is copied without modification. 0's are ignored.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for i in range(0, 4):
            curr_column = self.matrix[self.rows[i]]
            curr_column = self.remove_from_list(curr_column, 0)
            curr_column = self.fill_in_zeros(curr_column, 0, 4)
            new_values = [0, 0, 0, 0]
            counter = 0
            need_to_skip = False
            #clears out 0s in the column
            #checks for numbers that are the same that are next to each other
            for k in range(0, 4):
                #skips iteration in for loop.
                if(need_to_skip):
                    need_to_skip = False
                    continue
                #0s are at the end, if hit then we are done with column
                elif(curr_column[k] == 0):
                    continue
                #checks to see if the numbers are the same in columns and combines them if they are the same. Sets flag to skip next number
                elif(k < 3 and curr_column[k] == curr_column[k + 1]):
                    value = curr_column[k] * 2
                    curr_column[k] = 0
                    curr_column[k + 1] = 0
                    new_values[counter] = value
                    counter += 1
                    need_to_skip = True
                #number is unique so it is added without modification to the new values column
                else:
                    new_values[counter] = curr_column[k]
                    counter += 1
            #assigns the new values to the board
            self.matrix[self.rows[i]] = new_values

    def right_movement(self):
        '''
        Performs a right movement, similar to the game 2048,
        on the matrix within the board object. The movement will go 
        through all rows in the matrix. The matrix is a list of 
        length 16 and is arranged in a 4x4 grid with position 0 in the 
        top left and the list extending right and ending with position 16
        in the bottom right. For each row, the slice associated 
        with has its 0's removed and not replaced. The row is then 
        appended with 0's until the length is 4. The row is then 
        reversed. Starting at the far right of the row, if the number 
        to the left is the same then the numbers are combined and the 
        result is copied to a new array with the number below being 
        deleted if not then the number is copied without 
        modification. 0's are ignored. The move is a left move with 
        the row reversed.
        
        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for i in range(0, 4):
            curr_column = self.matrix[self.rows[i]]
            #reverses and clears out 0s in the column, uses temp column to allow loop to execute correctly, otherwise 2 zeros in first positions creates problem
            curr_column.reverse()
            curr_column = self.remove_from_list(curr_column, 0)
            curr_column = self.fill_in_zeros(curr_column, 0, 4)
            new_values = [0, 0, 0, 0]
            counter = 0
            need_to_skip = False
            #checks for numbers that are the same that are next to each other
            for k in range(0, 4):
                #skips iteration in for loop.
                if(need_to_skip):
                    need_to_skip = False
                    continue
                #0s are at the end, if hit then we are done with column
                elif(curr_column[k] == 0):
                    continue
                #checks to see if the numbers are the same in columns and combines them if they are the same. Sets flag to skip next number
                elif(k < 3 and curr_column[k] == curr_column[k + 1]):
                    value = curr_column[k] * 2
                    curr_column[k] = 0
                    curr_column[k + 1] = 0
                    new_values[counter] = value
                    counter += 1
                    need_to_skip = True
                #number is unique so it is added without modification to the new values column
                else:
                    new_values[counter] = curr_column[k]
                    counter += 1
            #assigns the new values to the board
            new_values.reverse()
            self.matrix[self.rows[i]] = new_values

    def determine_move(self, move):
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
            self.up_movement()
            return True
        elif(move == "down"):
            self.down_movement()
            return True
        elif(move == "left"):
            self.left_movement()
            return True
        elif(move == "right"):
            self.right_movement()
            return True
        else:
            print("invalid move")
            return False

    def print_matrix(self):
        '''
        Prints a 4x4 matrix that is in the form of a list of length 16.
        The function slices the matrix into 4 slices each corressponding to
        a row then prints the rows sequentially starting with first row.

        Args:
            list - length 16
        Returns:
            None
        Raises:
            None
        '''
        row_one = slice(0, 4)
        row_two = slice(4, 8)
        row_three = slice(8, 12)
        row_four = slice(12, 16)
        print(self.matrix[row_one])
        print(self.matrix[row_two])
        print(self.matrix[row_three])
        print(self.matrix[row_four])

    def make_copy_matrix(self):
        '''
        Copies array of length 16 into another array of length 16
        
        Args: 
            new_matrix (list of length 16) matrix to be copied to
        Returns:
            new_matrix
        Raises: 
            None
        '''
        new_matrix = [x * 0 for x in range(len(self.matrix))]
        for i in range(0, 16):
            new_matrix[i] = self.matrix[i]
        return new_matrix