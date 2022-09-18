# Class "problem"
class Problem:

    def __init__(self, probNumber_in, maxLiterals_in, numVariables_in, numClauses_in, answer_in):
        self.probNumber = probNumber_in
        self.maxLiterals = maxLiterals_in
        self.numVariables = numVariables_in
        self.numClauses = numClauses_in
        self.answer = answer_in
        self.probArray = list()



# Function to read file
def readFile(filename):
    
    rFile = open(filename, "r")

    # value to hold number of problems
    numProblems = 0

    # array to hold all the info
    equation_list = list();
    temp = rFile.readline()

    # read and add to list
    while (temp):
        equation_list.append(temp.strip())
        if (temp[0]) == 'c':
            numProblems += 1
        temp = rFile.readline()

    rFile.close()
    return equation_list, numProblems



# parse a list into LIST OF CLASS PROBLEMS
def getProblems(equation_list, numProblems):
    return
