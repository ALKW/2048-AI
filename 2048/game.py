def remove_from_list(this_list, value):
    return [value for value in this_list if value != 0]

is_over = False
score = 0
for i in reversed(range(0, 4)):
    print(i)
curr_column = [0,0,2,4]
curr_column = remove_from_list(curr_column, 0)
print(curr_column)