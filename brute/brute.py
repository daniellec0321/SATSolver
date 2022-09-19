import sys

# Class "problem"
class Problem:

    def __init__(self, probNumber_in, maxLiterals_in, numVariables_in, numClauses_in, answer_in):
        self.probNumber = int(probNumber_in)
        self.maxLiterals = int(maxLiterals_in)
        self.numVariables = int(numVariables_in)
        self.numClauses = int(numClauses_in)
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



# function that returns if a problem is satisfied given the variables
# currProblem is a Problem object
# assignments is an array of integers to represent the current variables assignments
# returns a boolean value: true if it is satisfiable, false if not
def verifyWFF(currProblem, assignments):

    # loop through the prob array of current problem
    for clause in currProblem.probArray:

        # return value of clause
        clauseRet = False

        # loop through the clause until a zero is hit
        for literal in clause:
            
            if literal == 0:
                break

            # get absolute value and negation
            val = abs(literal)
            negation = (literal < 0)

            # test if this literal evaluates to true
            if negation:
                if assignments[val-1] == 0:
                    clauseRet = True
                    break
                    
            else:
                if assignments[val-1] == 1:
                    clauseRet = True
                    break

        # if clause_ret is still false, then it is unsatisfiable
        if clauseRet == False:
            return False

    # if got through every clause, then return true
    return True



# This function prints the result of our current problem solver
# currProblem is a Problem object
# result is a boolean value representing if the problem was satisfiable or not
# return if the the two evaluations agreed
def writeOutput(currProblem, result):

    print("---------------------------------")
    print("Analyzing problem " + str(currProblem.probNumber) + "...")
    print("Problem " + str(currProblem.probNumber) + " evaluated to be " + str(result))

    # Check against answer in currProblem
    if (currProblem.answer == 'U' and result == False) or (currProblem.answer == 'S' and result == True):
        print("This evaluation is CORRECT")
        print("")
        return True
    else:
        print("This evaluation is INCORRECT")
        print("")
        return False



#################
# FUNCTION MAIN #
#################
def main():

    # Test command line input
    if len(sys.argv) != 3:
        print("Not correct amount of inputs.")
        return

    # get command line input
    filename = sys.argv[1]
    suppressOutput = sys.argv[2]
    if suppressOutput == 0:
        suppressOutput = True
    else:
        suppressOutput = False

    # get problem list
    probList = getProblems(filename)

    # loop through list to get results
    for problem in probList:
            
        problemRes = False

        # get each assignment
        for i in range(0, 2**problem.numVariables):

            # test assignment
            assignment = generateAssignment(problem, i)
            assignmentRes = verifyWFF(problem, assignment)

            # if true, then it is satisfiable
            if assignmentRes == True:
                problemRes = True
                break

        # if output not supressed, print results
        if suppressOutput == False:

            test = writeOutput(problem, problemRes)

            if test == False:
                print("ERROR")
                return



main()
