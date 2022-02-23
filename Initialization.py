import Services


def row_results():
    # Assumes two digit input <number_correct><number_incorrect>
    first_result = Services.get_input("Enter the result for 123: ")
    second_result = Services.get_input("Enter the result for 456: ")
    third_result = Services.get_input("Enter the result for 789: ")

    # Return the row results as a list of strings
    return [str(first_result), str(second_result), str(third_result)]


# Return a list specifying how many numbers in a "row" are part of the code
def determine_frequencies(results):
    frequencies = list(map(Services.int_string_sum, results))
    return frequencies


# Expects list of string results from codes 123, 456, 789 respectively
def determine_positions(results):
    positions = [set(), set(), set()]

    # Determine which numbers can possibly be at [first, second, third] position
    for i, num in enumerate([x for x in range(1, 10)]):
        result_int_list = Services.string_to_int_list(results[i // 3])
        position = i % 3

        # Check to see if there is at least 1 correct or incorrect number
        if (sum(result_int_list) != 0):
            num_correct = result_int_list[0]
            num_incorrect = result_int_list[1]

            # Only correct
            if (num_correct != 0 and num_incorrect == 0):
                # Add number to current position
                positions[position].add(str(num))

            # Only incorrect
            elif (num_correct == 0 and num_incorrect != 0):
                # Add number to all positions other than the current
                for j in [x for x in range(3) if x != position]:
                    positions[j].add(str(num))

            # Mix of correct and incorrect
            else:
                # Add number to all positions
                list(map(lambda s: s.add(str(num)), positions))

    return positions


# Assumes 123, 456, 789 code entries
def check_correct(initial_results):
    # Check for correct
    code = ""
    max_sum = 0
    num_correct = 0
    num_incorrect = 0

    # From initial codes, determine which one to use to generate possibilities
    for i, result in enumerate(initial_results):
        attempt_sum = Services.int_string_sum(result)
        result_list = list(result)

        if (attempt_sum > max_sum):
            code = "".join([str((3 * i) + 1),
                            str((3 * i) + 2),
                            str((3 * i) + 3)])
            max_sum = attempt_sum
            num_correct = int(result_list[0])
            num_incorrect = int(result_list[1])

    return code, num_correct, num_incorrect
