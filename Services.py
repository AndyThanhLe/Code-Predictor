# Provide functions to other classes

def get_input(message):
    user_input = input(message)
    return user_input


# Assumes elements of string can be typecasted to integer
def string_to_int_list(int_string):
    return [int(x) for x in list(int_string)]


# Assumes elements of string can be typecasted to integer
def int_string_sum(int_string):
    return sum([int(x) for x in list(int_string)])


# Generate rows 123, 456, 789 given 0, 1, 2 respectively
def row_code_set(row):
    code_set = {str((3 * row) + 1),
                str((3 * row) + 2),
                str((3 * row) + 3)}

    return code_set


# Return the row a code number belongs to
def code_row(str_num):
    row = (int(str_num) - 1) // 3
    return row
