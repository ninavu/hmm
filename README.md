# Viterbi algorithm: viterbi.py

The program has global variables, which all belong to the Hidden Markov Model:
1. 2 states in the list named "die_type", which are 'F' and 'L'
2. Transition probabilities of 2 states in the dictionary of dictionary named "t_prob"
3. Emission probabilities of all variables of each state in the dictionary of dictionary named "e_prob
4. List of die numbers from 1 to 6
5. Initial equal probability to 2 states

The program has the following functions:
1. genDieNumbers(n): simulates the dealer to generate a sequence of n throws based on the given HMM
2. viterbi(seq, n): implements the Viterbi algorithm to decode the type of dies used by the dealer for each number
3. maxVal(x, y): returns the max value and variable
4. to_string(L): returns a string converted from a list

For viterbi(seq, n), we can uncomment all comments in main() to test our predictions vs. the generated dies. The results will be written in "output.txt".

In the main() function, the program calculates the overall accuracy and MCC of the Viterbi algorithm by generating sequences of n dies 10 times. It will then calculate the average accuracy and MCC of all sequences of size n and write the results in "output.txt".

All screenshots of the examples and annonated graphs are in the PDF file called "Report".
