'''Board class for representing the 2048 board'''
import random
import copy

from examples.game_2048 import error

class Board():
    '''
    Inherits from the matrix class in order to give it more functionality as a board

    The board itself is a "matrix" under the hood (a 1d list in python with members dividing
    the list)
    '''

    ROW_ONE = slice(0, 4)
    ROW_TWO = slice(4, 8)
    ROW_THREE = slice(8, 12)
    ROW_FOUR = slice(12, 16)
    ROWS = [ROW_ONE, ROW_TWO, ROW_THREE, ROW_FOUR]

    COLUMN_ONE = slice(0, 16, 4)
    COLUMN_TWO = slice(1, 16, 4)
    COLUMN_THREE = slice(2, 16, 4)
    COLUMN_FOUR = slice(3, 16, 4)
    COLUMNS = [COLUMN_ONE, COLUMN_TWO, COLUMN_THREE, COLUMN_FOUR]

    def __init__(self, board=None):
        if board is not None:
            if len(board) != 16:
                print("Invalid board length given to instantiate matrix")
                raise error.LengthError("Board length of " + str(len(board)) + " is not the correct\
                                     board length")
            self.matrix = copy.deepcopy(board)
        else:
            self.matrix = [
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0
            ]

    @classmethod
    def choose(cls):
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
        if probability >= 2:
            return 2
        return 4

    @classmethod
    def pick_position(cls):
        '''
        Picks a random number between 0 and 15 in order to pick a position on the board

        Args:
            None
        Returns:
            (int) - random between 0 and 15
        Raises:
            None
        '''
        position = random.randint(0, 15)
        return position

    def spawn_number(self):
        '''
        Creates either a 4 or a 2 anywhere a zero is in the list

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        number_to_insert = self.choose()
        position = random.randint(0, 15)
        while self.matrix[position] != 0:
            if self.is_full():
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
        if min(self.matrix) == 0:
            return False

        for column_slice in self.COLUMNS:
            column = self.matrix[column_slice]
            if self.can_move(column):
                return False

        for row_slice in self.ROWS:
            row = self.matrix[row_slice]
            if self.can_move(row):
                return False

        return True

    def can_move(self, data):
        '''
        Checks if it is possible to move on the board or not

        Args:
            data - (list) - the list of integers that make up the board
        Returns:
            (Boolean) - true if it is possible to move
                        false otherwise
        Raises:
            None
        '''
        # Check for if we can move horizontally
        if self.can_move_helper(data):
            return True

        # Transpose the board
        row_length = 4
        new_data = []
        for row_num in range(0, row_length):
            for j in range(row_num, len(data), row_length):
                new_data.append(data[j])
        data = new_data

        # check for if we can move vertically
        if self.can_move_helper(data):
            return True

        return False

    @classmethod
    def can_move_helper(cls, data):
        '''
        this
        '''
        curr = data[0]
        counter = 0
        for entry in data[1:]:
            # If we reach the end of a row, then continue
            if counter % 4 == 0:
                curr = entry
                continue
            # If an entry in a row is the same as the one next to it, we can move
            elif curr == entry:
                return True
            # Otherwise check the next one
            else:
                curr = entry
            counter += 1
        return False

    @classmethod
    def extend_with_to(cls, arr, value, length):
        '''
        Appends values to the end of a list up to a specified length

        Args:
            arr (list) - list to be modified
            value (int) - value to be appeneded to end of list
            length (int) - target length of list
        Returns:
            (list) - arr with values appended
        Raises:
            None
        '''
        while len(arr) <= length:
            arr.append(value)
        return arr

    @classmethod
    def remove_from_list(cls, this_list, value):
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

    @classmethod
    def can_move_at_line(cls, line):
        '''
        Determines if we can move in a row or column or not. Does not compute the result

        Args:
            line - (list) - row or column to compute if its possible to move or not
        Returns:
            (Boolean) - True if we can move. False if we cannot
        Raises:
            None
        '''
        curr = line[0]
        for entry in line[1:]:
            # Skip over 0's
            if entry == 0:
                continue

            # If we find the same number then we are done
            if curr == entry:
                return True

            # If we find a different number, then we are now looking for a matching number
            curr = entry

        # If we reach the end, then we never found a mathc
        return False

    @classmethod
    def execute_move(cls, curr_list):
        '''
        Executes the corresponding move given the column or row

        Args:
            curr_list - (list) - the row or column that is being executed upon
        Returns:
            (list) - The new values for the column after the move is executed
        Raises:
            None
        '''
        # Used to store the new values after a movement has occurred
        new_values = [0, 0, 0, 0]
        counter = 0

        # When two numbers are combined we need to skip over the number that was used to combine
        need_to_skip = False

        # checks for numbers that are the same that are next to each other
        for cell_index in range(0, 4):
            # skips iteration in for loop.
            if need_to_skip:
                need_to_skip = False
                continue
            #0s are at the end, if hit then we are done with column
            if curr_list[cell_index] == 0:
                break
            # checks to see if the numbers are the same in columns and combines them if they
            # are the same. Sets flag to skip next number
            if cell_index < 3 and curr_list[cell_index] == curr_list[cell_index + 1]:
                value = curr_list[cell_index] * 2
                curr_list[cell_index] = 0
                curr_list[cell_index + 1] = 0
                new_values[counter] = value
                counter += 1
                need_to_skip = True
            # number is unique so it is added without modification to the new values column
            else:
                new_values[counter] = curr_list[cell_index]
                counter += 1

        return new_values

    def is_valid(self, move):
        '''
        Determines if a move is valid or not

        Args:
            move - (string) - the move in question
        Returns:
            (Boolean) - if the move is possible or not
        Raises:
            None
        '''
        test_board = copy.deepcopy(self)
        test_board.exec_move(move)

        if test_board.matrix != self.matrix:
            return True
        return False

    def up_movement(self):
        '''
        Performs an up movement on the matrix within the board object. The movement will go through
        all columns in the matrix. The matrix is a 1d list of length 16 and is arranged using
        slices in a 4x4 grid with position 0 in the top left and the list extending right and
        ending with position 16 in the bottom right. For each column the slice associated with has
        its 0's removed and not replaced. The column is then appended with 0's until the length is
        4. Starting at the top of the column, if the number below is the same then the numbers are
        combined and the result is copied to a new array with the number below being deleted if not
        then the number is copied without modification. 0's are ignored.

        Column indices in terms of board orientation:
        0
        1
        2
        3

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for col_index in range(0, 4):
            # Get a column
            curr_column = self.matrix[self.COLUMNS[col_index]]

            # Remove all the zeros in the list as 0's are ignored in matching adjacent pairs
            # [2 0 2] is equivalent to [2 2] when it comes to moves
            # Then extend the row if 0's were removed. Essentially putting 0's at the end
            curr_column = self.remove_from_list(curr_column, 0)
            curr_column = self.extend_with_to(curr_column, 0, 4)

            new_values = self.execute_move(curr_column)

            # assigns the new values to the column
            self.matrix[self.COLUMNS[col_index]] = new_values

    def down_movement(self):
        '''
        Performs a down movement on the matrix within the board object. The movement will go through
        all columns in the matrix. The matrix is a 1d list of length 16 and is arranged using
        slices in a 4x4 grid with position 0 in the top left and the list extending right and
        ending with position 16 in the bottom right. For each column the slice associated with has
        its 0's removed and not replaced. The column is then appended with 0's until the length is
        4. Starting at the bottom of the column, if the number above is the same then the numbers
        are combined and the result is copied to a new array with the number below being deleted if
        not then the number is copied without modification. 0's are ignored.

        Column indices in terms of board orientation:
        0
        1
        2
        3

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for col_index in range(0, 4):
            curr_column = self.matrix[self.COLUMNS[col_index]]
            # reverses and clears out 0s in the column, uses temp column to allow loop to execute
            # correctly otherwise 2 zeros in first positions creates problem. List is reveresed to
            # account for opposite Direction of move
            curr_column.reverse()
            curr_column = self.remove_from_list(curr_column, 0)
            curr_column = self.extend_with_to(curr_column, 0, 4)

            new_values = self.execute_move(curr_column)

            # Reverse the row back as we reversed it earlier
            new_values.reverse()

            # assigns the new values to the column
            self.matrix[self.COLUMNS[col_index]] = new_values

    def left_movement(self):
        '''
        Performs a left movement, similar to the game 2048, on the matrix within the board object.
        The movement will go through all rows in the matrix. The matrix is a list of length 16 and
        is arranged in a 4x4 grid with position 0 in the top left and the list extending right and
        ending with position 16 in the bottom right. For each row, the slice associated with has
        its 0's removed and not replaced. The row is then appended with 0's until the length is 4.
        Starting at the far right of the row, if the number to the left is the same then the
        numbers are combined and the result is copied to a new array with the number below being
        deleted if not then the number is copied without modification. 0's are ignored.

        Row indices in terms of board orientation:
        0 1 2 3

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for row_index in range(0, 4):
            curr_row = self.matrix[self.ROWS[row_index]]

            # The same operation except we operate on rows instead of columns
            curr_row = self.remove_from_list(curr_row, 0)
            curr_row = self.extend_with_to(curr_row, 0, 4)

            new_values = self.execute_move(curr_row)

            # assigns the new values to the row
            self.matrix[self.ROWS[row_index]] = new_values

    def right_movement(self):
        '''
        Performs a right movement, similar to the game 2048, on the matrix within the board object.
        The movement will go through all rows in the matrix. The matrix is a list of length 16 and
        is arranged in a 4x4 grid with position 0 in the top left and the list extending right and
        ending with position 16 in the bottom right. For each row, the slice associated with has
        its 0's removed and not replaced. The row is then appended with 0's until the length is 4.
        Starting at the far left of the row, if the number to the right is the same then the
        numbers are combined and the result is copied to a new array with the number below being
        deleted if not then the number is copied without modification. 0's are ignored.

        Row indices in terms of board orientation:
        0 1 2 3

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        for row_index in range(0, 4):
            curr_row = self.matrix[self.ROWS[row_index]]
            # reverses and clears out 0s in the column, uses temp column to allow loop to execute
            # correctly, otherwise 2 zeros in first positions creates problem
            curr_row.reverse()
            curr_row = self.remove_from_list(curr_row, 0)
            curr_row = self.extend_with_to(curr_row, 0, 4)

            new_values = self.execute_move(curr_row)

            # Reverse the row back as we reversed it earlier
            new_values.reverse()

            # assigns the new values to the row
            self.matrix[self.ROWS[row_index]] = new_values

    def exec_move(self, move):
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
        if move == "up":
            self.up_movement()
            return True
        if move == "down":
            self.down_movement()
            return True
        if move == "left":
            self.left_movement()
            return True
        if move == "right":
            self.right_movement()
            return True
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
        print(self.matrix[Board.ROW_ONE])
        print(self.matrix[Board.ROW_TWO])
        print(self.matrix[Board.ROW_THREE])
        print(self.matrix[Board.ROW_FOUR])

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
