# Class "problem"
class Problem:

    def __init__(self, probNumber_in, maxLiterals_in, numVariables_in, numClauses_in, answer_in):
        self.probNumber = probNumber_in
        self.maxLiterals = maxLiterals_in
        self.numVariables = numVariables_in
        self.numClauses = numClauses_in
        self.answer = answer_in
        self.probArray = list()



# parse a list into LIST OF CLASS PROBLEMS
def getProblems(filename):

    rFile = open(filename, "r")

    # values to hold problem info
    numProblems = 0
    problemList = list()

    # initialize readings
    celems = rFile.readline().strip().split(" ")
    pelems = rFile.readline().strip().split(" ")
    currProblem = Problem(celems[1], celems[2], pelems[2], pelems[3], celems[3])

    currLine = rFile.readline().strip()
    while(currLine):

        # if equation list at counter starts with c, reset
        if currLine[0] == 'c':
           
            problemList.append(currProblem)
            celems = currLine.split(" ")
            currProblem = Problem(int(celems[1]), int(celems[2]), -1, -1, celems[3])

        # if starts with p, set all other class elements
        elif currLine[0] == 'p':

            pelems = currLine.split(" ")
            currProblem.numVariables = int(pelems[2])
            currProblem.numClauses = int(pelems[3])
    
        # otherwise, append equation to current problem
        else: 

            eq = currLine.split(",")
            for i in range(0, len(eq)):
                eq[i] = int(eq[i])
            currProblem.probArray.append(eq)

        # read next line
        currLine = rFile.readline().strip()

    # append last problem to list
    problemList.append(currProblem)

    return problemList



# function that generates the next assignment of variables
# currProblem is a Problem object
# attemptNumber is an integer
# returns an array of integers that represent the assignments
def generateAssignment(currProblem, attemptNumber):

    # get binary representation in a string form
    binString = str(bin(attemptNumber))[2:]

    # make binary string same length as num variables
    temp = ""
    for i in range(0, currProblem.numVariables - len(binString)):
        temp += '0'
    binString = temp + binString

    # convert string to array of ints
    varList = list()
    for char in binString:
        varList.append(int(char))

    return varList
