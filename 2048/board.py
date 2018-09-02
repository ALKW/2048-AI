import random

class Matrix:
    matrix = [2, 0, 0, 0, 
    2, 0, 0, 0, 
    2, 0, 0, 0, 
    2, 0, 0, 0]
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

    def choose(self):
        probability = random.randrange(1, 11)
        if(probability >= 2):
            return 2
        else:
            return 4

    def pick_position(self):
        p = random.randint(0, 16)
        return p

class Board(Matrix):
    def spawn_number(self):
        number_to_insert = Matrix.choose(Board.matrix)
        position = random.randint(0, 16)
        while(self.matrix[position] != 0):
            position = Matrix.pick_position(Board.matrix)
        self.matrix[position] = number_to_insert
    
    def is_full(self):
        if (min(self.matrix) == 0):
            return False
        else:
            return True
    
    def up_movement(self):
        for i in range(0, 4):
            curr_column = self.matrix[self.columns[i]]
            new_values = curr_column
            counter = 0
            for j in range(1, 4):
                if(curr_column[j] == 0):
                    del new_values[j]
                    new_values.append(0)
            for k in range(1, 4):
                if(new_values[k] == 0):
                    continue
                elif(curr_column[j] == curr_column[j + 1]):
                    value = curr_column[j] * 2
                    curr_column[j] = 0
                    curr_column[j + 1] = 0
                    new_values[counter] = value
                    counter += 1
                else:
                    new_values[counter] = curr_column[j]
            self.matrix[self.columns[i]] = new_values
        print("Completed Up Movement")
    
    def down_movement(self):
        for i in reversed(range(0, 3)):
            curr_column = self.matrix[self.columns[i]]
            new_values = [0, 0, 0, 0]
            counter = 3
            for j in range(0, 3):
                if(curr_column[j] == 0):
                    continue
                else:
                    if(curr_column[j] == curr_column[j - 1]):
                        value = curr_column[j] * 2
                        curr_column[j] = 0
                        curr_column[j - 1] = 0
                        new_values[counter] = value
                        counter -= 1
            self.matrix[self.columns[i]] = new_values
        print("Completed Down Movement")

    def left_movement(self):
        pass

    def right_movement(self):
        for i in reversed(range(0, 3)):
            curr_row = self.matrix[self.rows[i]]
            new_values = [0, 0, 0, 0]
            counter = 3
            for j in range(0, 3):
                if(curr_row[j] == 0):
                    continue
                else:
                    if(curr_row[j] == curr_row[j - 1]):
                        value = curr_row[j] * 2
                        curr_row[j] = 0
                        curr_row[j - 1] = 0
                        new_values[counter] = value
                        counter -= 1
            self.matrix[self.rows[i]] = new_values
        print("Completed Right Movement")

def print_matrix_4_rows(m):
    row_one = slice(0, 4)
    row_two = slice(4, 8)
    row_three = slice(8, 12)
    row_four = slice(12, 16)
    print(m[row_one])
    print(m[row_two])
    print(m[row_three])
    print(m[row_four])


B = Board()
print_matrix_4_rows(B.matrix)
B.down_movement()
print_matrix_4_rows(B.matrix)
B.up_movement()
print_matrix_4_rows(B.matrix)
