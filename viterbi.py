import math
import random

# global variables
die_type = ['F', 'L']
die_num = list(range(1, 7))
initial_prob = [1/2] * 2
t_prob = {'F': {'F': 0.9, 'L': 0.1} ,'L': {'F': 0.2, 'L': 0.8}} 
e_prob = {'F': [1/6] * 6, 'L': [1/10] * 5 + [1/2]}

# this function simulates the dealer to generate a sequence of n throws based on the given HMM
def genDieNumbers(n):
    if n == 0:
        return None

    dieSeq, numSeq = [], []
    cur_die, cur_num = '', 0

    for i in range(n):
        if i == 0:
            cur_die = random.choices(die_type, weights=initial_prob, k=1)[0]
        
        dieSeq.append(cur_die)
        prob = list(t_prob[cur_die].values())
        cur_num = random.choices(die_num, weights=e_prob[cur_die], k=1)[0]
        cur_die = random.choices(die_type, weights=prob, k=1)[0]
        numSeq.append(cur_num)

    return numSeq, dieSeq

# this function returns the max value and variable
def maxVal(x, y):
    val = 0
    die = ''
    if x >= y:
        val = x
        die = 'F'
    else:
        val = y
        die = 'L'
    return val, die

# this function implements the Viterbi algorithm to decode the type of dies used by the dealer for each number
def viterbi(seq, n):
    W_matrix = {'F': [0] * (n+1), 'L': [0] * (n+1)}
    decode = {'F': [0] * (n+1), 'L': [0] * (n+1)}

    for i in range(1, n+1):
        cur_num = seq[i-1]
        for j in range(1, 3):
            if j == 1: die = 'F'
            else: die = 'L'

            e_log = math.log2(e_prob[die][cur_num-1])
            if i == 1:
                W_matrix[die][i] = math.log2(1) + math.log2(initial_prob[0]) + e_log
                decode[die][i] = 'B'
            else:
                W_f = W_matrix['F'][i-1] + math.log2(t_prob['F'][die]) + e_log
                W_l = W_matrix['L'][i-1] + math.log2(t_prob['L'][die]) + e_log

                W = maxVal(W_f, W_l)
                W_matrix[die][i] = W[0]
                decode[die][i] = W[1]

    last_col = maxVal(W_matrix['F'][n], W_matrix['L'][n])[1]
    guess = [last_col]

    for i in range(n, 1, -1):
        backtrack = decode[last_col]
        guess.insert(0, backtrack[i])

    return guess

# this function returns a string converted from a list
def to_string(L):
    s = ""
    for i in range(len(L)):
        s += str(L[i])
    return s

def main():
    fout = open("output.txt", "w")
    fout.write("\n")
    # rolls = [6, 2, 6]
    # dies = ['L', 'L', 'L']
    # n = 100
    # dealer = genDieNumbers(n)
    # rolls = dealer[0]
    # dies = dealer[1]
    # prediction = viterbi(rolls, len(rolls))

    # fout.write("Rolls      " + to_string(rolls) + "\n")
    # fout.write("Die        " + to_string(dies) + "\n")
    # fout.write("Viterbi    " + to_string(prediction) + "\n")

    for n in range(100, 2000, 100):
        total_acc, total_MCC = 0, 0
        avg_acc, avg_MCC = 0, 0
        for k in range(10):
            dealer = genDieNumbers(n)
            rolls = dealer[0]
            dies = dealer[1]
            prediction = viterbi(rolls, n)
            TP, TN, FP, FN = 0, 0, 0, 0

            for i in range(n):
                if dies[i] == 'F':
                    if prediction[i] == dies[i]: TP += 1
                    else: FN += 1
                else:
                    if prediction[i] == dies[i]: TN += 1
                    else: FP += 1
            
            accuracy = (TP + TN) / (TP + TN + FP + FN) * 100
            r = (TP + FN)*(TP + FP)*(TN + FP)*(TN + FN)
            MCC = 0
            if r != 0:
                MCC = (TP * TN - FP * FN) / math.sqrt(r)
            
            total_acc += accuracy
            total_MCC += MCC
        
        avg_acc = round(total_acc / 10, 2)
        avg_MCC = round(total_MCC / 10, 5)
        fout.write("For input size " + str(n) + ", ")
        fout.write("average accuracy: " + str(avg_acc) + "% ")
        fout.write("and average MCC: " + str(avg_MCC) + "\n")
            
    fout.close()
main()