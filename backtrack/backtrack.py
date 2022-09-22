import sys
import time



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
# filename is a string that contains path to file
# returns a list of Problems
def getProblems(filename):

    rFile = open(filename, "r")

    # The list of problems we will return
    problemList = list()

    # initialize readings
    celems = rFile.readline().strip().split(" ")
    pelems = rFile.readline().strip().split(" ")
    currProblem = Problem(celems[1], celems[2], pelems[2], pelems[3], celems[3])

    # Loop through file
    currLine = rFile.readline().strip()
    while(currLine):

        # if current line starts with c, begin a new Problem
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



# This function prints the result of our current problem solver
# currProblem is a Problem object
# result is a boolean value representing if the problem was satisfiable or not
# return if the the two evaluations agreed
def writeOutput(currProblem, result):

    print("-----------------------------------------")
    print("Analyzing problem " + str(currProblem.probNumber) + "...")
    if result == False:
        print("Problem " + str(currProblem.probNumber) + " evaluated to be UNSATISFIABLE")
    else:
        print("Problem " + str(currProblem.probNumber) + " evaluated to be SATISFIABLE")

    # Check against answer in currProblem
    if (currProblem.answer == 'U' and result == False) or (currProblem.answer == 'S' and result == True):

        print("This evaluation is CORRECT\n")
        return True

    elif (currProblem.answer == '?'):

        print("")
        return True

    else:

        print("This evaluation is INCORRECT\n")
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
    if suppressOutput == '0':
        suppressOutput = True
    else:
        suppressOutput = False

    # get problem list
    probList = getProblems(filename)

    # list to hold each time for each problem
    probTimes = list()

    # loop through list to get results
    for problem in probList:

        problemRes = False

        # start timer for current problem
        startTime = time.time()

        ################ evaluate here ################

        # end the timer and add to array
        endTime = time.time()
        probTimes.append((endTime - startTime)*(10**6))

        # if output not supressed, print results
        if suppressOutput == False:
            test = writeOutput(problem, problemRes)



main()
