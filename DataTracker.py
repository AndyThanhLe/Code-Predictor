# Class stores prediction data and contains methods necessary for the 
# maintenance and mutation of the data
class DataTracker:
    def __init__(self, frequencies, position_possibilities):
        # Dictionary tracking weight of number at each position
        self.number_weights = {"1": [0, 0, 0], "2": [0, 0, 0], "3": [0, 0, 0],
                               "4": [0, 0, 0], "5": [0, 0, 0], "6": [0, 0, 0],
                               "7": [0, 0, 0], "8": [0, 0, 0], "9": [0, 0, 0]}
        # List specifying how many numbers in a "row" are part of the code
        self.row_frequencies = frequencies
        # List of sets specifying possible code numbers in each position
        self.position_possibilities = position_possibilities
        # Set of assumed correct numbers
        self.assumed_correct = set()
        # Stack containing possible code combinations
        self.possibilities = []
        # Set of attempts
        self.attempts = {"123", "456", "789"}

    # Return the key with the greatest weight at a certain position
    def get_greatest_weight(self, str_nums, position):
        return max(str_nums, key=lambda x: self.number_weights[x][position])

    # Return the quantity of numbers in a row that is part of the code
    def get_row_freqs(self):
        return self.row_frequencies

    # Adjust the current weight of a number in a position
    def add_number_weight(self, str_num, position):
        # 100 chosen as arbitrarily large number
        self.number_weights[str_num][position] += 100

    # Return possible numbers in each code position
    def get_position_possibilities(self):
        return self.position_possibilities

    # Return the numbers assumed to be correct
    def get_assumed_correct(self):
        return self.assumed_correct

    # Set the numbers that are assumed to be correct
    def set_assumed_correct(self, assumptions):
        self.assumed_correct = assumptions

    # Return the list of possibilities
    def get_possibilities(self):
        return self.possibilities

    # Set a new list of possibilities
    def set_possibilities(self, possibilities):
        self.possibilities = possibilities
        self.refresh_possibilities

    # Peek possibility at top of stack
    def get_possibility(self):
        return self.possibilities[-1]

    def remove_possibility(self):
        self.possibilities.pop()

    # Remove possibility if there are no possibilities at a certain position
    def refresh_possibilities(self):
        for possibility in self.possibilities:
            for pps in possibility:
                if len(pps) == 0:
                    self.possibilities.remove(possibility)

    def discard_at_position(self, str_num, position):
        self.position_possibilities[position].discard(str_num)
        for possibility in self.possibilities:
            possibility[position].discard(str_num)

        self.refresh_possibilities()

    def discard_number(self, str_num):
        list(map(lambda x: x.discard(str_num), self.position_possibilities))
        for possibility in self.possibilities:
            list(map(lambda x: x.discard(str_num), possibility))

    # Return boolean specifying if attempt is unique
    def unique_attempt(self, code):
        if code not in self.attempts:
            return True
        return False

    # Add an attempt
    def add_attempt(self, code):
        self.attempts.add(code)
