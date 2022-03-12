from DataTracker import DataTracker
import Initialization
import random
import Services


# Results for 123, 456, 789 codes respectively
results = Initialization.row_results()
frequencies = Initialization.determine_frequencies(results)
positions = Initialization.determine_positions(results)

# Instantiate DataTracker
dt = DataTracker(frequencies, positions)


# Generate list of remaining frequencies to satisfy
def generate_frequencies():
    freqs = []

    for i, freq in enumerate(dt.get_row_freqs()):
        freqs += [i] * freq

    random.shuffle(freqs)

    return freqs


# Generate possible code combinations
# Note: Generated codes may have an empty set
def generate_possibilities(code, num_correct, num_incorrect):
    code_list = list(code)
    possibilities = []

    if num_correct == 1:
        dt.set_assumed_correct(set(code_list))

        for i, str_num in enumerate(code_list):
            possibility = [set(), set(), set()]
            selected = set()
            remaining_positions = {0, 1, 2}
            accounted_incorrect = 0

            # Assume number at position i to be correct
            possibility[i] = {str_num}
            selected.add(str_num)
            remaining_positions.discard(i)

            # Iterate through each number
            for j in range(len(code_list)):
                if i != j:
                    other_position = next(iter(remaining_positions - {i, j}))

                    # Still incorrect numbers to consider
                    if accounted_incorrect < num_incorrect:
                        # Assign assumed incorrect to a possible corrected position
                        code_num = code_list[other_position]
                        possibility[j] = {code_num}
                        selected.add(code_num)
                        accounted_incorrect += 1
                    # Satisfy remaining row frequencies
                    else:
                        # Assign set of possible numbers at the position
                        pps = dt.get_position_possibilities()[j] - selected
                        possibility[j] = pps

                    remaining_positions.discard(other_position)

            possibilities.append(possibility)

    elif num_correct == 2:
        dt.set_assumed_correct(set(code_list))

        # Note: Number of incorrect cannot be greater than 0
        # Keep two numbers and their positions the same
        for i, str_num in enumerate(code_list):
            possibility = [set(), set(), set()]

            # Assign position possibilities
            for j in range(len(code_list)):
                if i == j:
                    pps = dt.get_position_possibilities()[i] - set(code_list)
                    possibility[i] = pps
                else:
                    possibility[j] = {code_list[j]}

            possibilities.append(possibility)

    # Zero correct
    else:
        # Note: There will be at least one incorrect
        for i, str_num in enumerate(code_list):
            for j in range(len(code_list)):
                if i == j:
                    dt.discard_at_position(str_num, i)
                else:
                    dt.add_number_weight(str_num, j)

        code_set = set(list(code))
        other_locations = [set(), set(), set()]
        # Generate a list of sets specifying the possible corrected positions
        # of the incorrect numbers
        for i, str_num in enumerate(code_list):
            other_locations[i] = code_set - {str_num}

        if num_incorrect == 1:
            # Assign the incorrect value at a possible corrected position
            for i, str_num in enumerate(code_list):
                for j in range(len(code_list)):
                    possibility = [set(), set(), set()]

                    if i != j:
                        possibility[j] = {str_num}

                        for i, pps in enumerate(possibility):
                            if len(pps) == 0:
                                possibility[i] = dt.get_position_possibilities()[i]

                        possibilities.append(possibility)

        elif num_incorrect == 2:
            for i in range(len(code_list)):
                remaining_positions = [0, 1, 2]
                remaining_positions.remove(i)
                pos_1 = remaining_positions[0]
                pos_2 = remaining_positions[1]

                for a in other_locations[pos_1]:
                    possibility = [set(), set(), set()]
                    selected = set()

                    possibility[pos_1] = {a}
                    selected.add(a)

                    for b in other_locations[pos_2]:
                        print(str(a) + ", " + str(b))
                        if b not in selected:
                            possibility[pos_2] = {b}
                            selected.add(b)
                            pps = dt.get_position_possibilities()[i] - selected
                            if len(pps) > 0:
                                possibility[i] = pps
                                print(possibility)
                                possibilities.append(possibility)

        elif num_incorrect == 3:
            for a in other_locations[0]:
                possibility = [{a}, set(), set()]
                selected = {a}

                for b in other_locations[1]:
                    if b not in selected:
                        possibility[1] = {b}
                        selected.add(b)

                        for c in other_locations[2]:
                            if c not in selected:
                                possibility[2] = {c}
                                possibilities.append(possibility)

        else:
            print("Something went wrong.")

    return possibilities


def make_prediction():
    code_list = ['', '', '']
    code_set = set()
    account_freqs = [0, 0, 0]
    possibility = dt.get_possibility()

    print(possibility)

    # Account for position possibilities with only one possibility
    for i, pps in enumerate(possibility):
        if len(pps) == 0:
            print("Something went wrong.")
        elif len(pps) == 1:
            str_num = next(iter(pps))
            row = Services.code_row(str_num)

            code_list[i] = str_num
            code_set.add(str_num)
            account_freqs[row] += 1

    remaining_freqs = [x1 - x2 for (x1, x2) in zip(dt.get_row_freqs(), account_freqs)]

    while True:
        rows = []
        # List of remaining frequencies to fulfill
        for i, freq in enumerate(remaining_freqs):
            rows += [i] * freq
        random.shuffle(rows)

        possible_code = code_list
        code_complete = True

        for i, str_num in enumerate(code_list):
            # Set of possible numbers
            if str_num == '':
                r = rows.pop()
                focused_pps = possibility[i].intersection(Services.row_code_set(r)) - code_set

                if len(focused_pps) != 0:
                    code_num = dt.get_greatest_weight(focused_pps, i)
                    possible_code[i] = code_num
                    code_set.add(code_num)
                else:
                    code_complete = False

        code = "".join(possible_code)

        if code_complete and dt.unique_attempt(code):
            dt.add_attempt(code)
            break

    return code


# Check the initial code combinations and return the one with the largest sum
# of correct and incorrect number positions
print(results)
code, num_correct, num_incorrect = Initialization.check_correct(results)

# Generate initial possibilities
dt.set_possibilities(generate_possibilities(code, num_correct, num_incorrect))

max_sum = num_correct + num_incorrect

while True:
    # Make a prediction and get the result
    print(dt.get_possibilities())
    code = make_prediction()
    print("Predicted code: " + code)
    result = Services.get_input("Enter result: ")

    code_list = list(code)
    result_list = list(result)
    result_sum = Services.int_string_sum(result)
    attempt_num_correct = int(result_list[0])
    attempt_num_incorrect = int(result_list[1])

    if attempt_num_correct == 3:
        break

    if result_sum < max_sum:
        if result_sum == 0:
            for str_num in code_list:
                dt.discard_number(str_num)

        if len(dt.get_possibilities()) > 1:
            dt.remove_possibility()

        dt.refresh_possibilities()

    elif result_sum > max_sum:
        max_sum = result_sum
        num_correct = attempt_num_correct
        num_incorrect = attempt_num_incorrect
        dt.set_possibilities(generate_possibilities(code, attempt_num_correct, attempt_num_incorrect))

    else:  # Same sum
        if attempt_num_correct < num_correct:
            dt.remove_possibility()

        elif attempt_num_correct > num_correct:
            # Regenerate possibilities
            num_correct = attempt_num_correct
            num_incorrect = attempt_num_incorrect
            dt.set_possibilities(generate_possibilities(code, attempt_num_correct, attempt_num_incorrect))
        else:  # Result is the same
            if len(dt.get_possibilities()) > 1:
                dt.remove_possibility()
            else:
                for i, str_num in enumerate(code_list):
                    print(dt.get_assumed_correct())
                    if str_num not in dt.get_assumed_correct():
                        dt.discard_at_position(str_num, i)
