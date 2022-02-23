# Code Predictor

Program suggests the prediction of a randomly generated 3-digit code based on feedback.

This feedback involves 2 numbers indicating:
1. the number of correct digits in the predicted code, and
2. the number of digits in the correct position in the code.

For instance, given a randomly generated code of "356", a prediction of "651" would yield
* 2 correct digits (5 and 6), and
* 1 digit in the correct spot (5).


# How It Works

It is given that the code consists of 3 unique digits from 1 to 9.

The first three predictions will be "123", "456", and "789". [^1] This is used to refine the predictions, where each code represents a subset of digits, and the feedback of the correct number of digits indicates the number of digits that need to be selected from each subset.

Then, predictions are made and adjusted accordingly based on the feedback increasing or decreasing.


# Technologies Used

* Sets
* Lists
* Tuples
* Dictionaries

* Map
* Enumerate
* Lamda Functions
* Zip


# Future Plans

Implement a GUI where the user inputs their code prediction and the resulting feedback.


[^1]: Any collection of 3, 3-item subsets such that their union consists of all digits 1 to 9 can be chosen with some modification to the code.