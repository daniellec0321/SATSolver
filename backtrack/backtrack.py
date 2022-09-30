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
        # self.occ = [0] * int(numVariables_in) # Only use this for backtracking
        self.occ = list() # Only use this for backtracking



# Class "variable" (holds a current variable value and its flags)
# vals will always be 0 or 1
class Var:

    def __init__(self, relativeVar, currVal):
        self.relativeVar = relativeVar
        self.currVal = currVal
        self.valsTried = [currVal]
        self.allValsTried = False

    def swapVal(self):
        self.currVal = (self.currVal + 1) % 2
        self.valsTried.append(self.currVal)
        if len(self.valsTried) >= 2:
            self.allValsTried = True



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

    # initialize unordered list to count occurrences of each number
    occ = [0] * currProblem.numVariables

    # Loop through file
    currLine = rFile.readline().strip()
    while(currLine):

        # if current line starts with c, begin a new Problem
        if currLine[0] == 'c':

            # set occ into current problems using dictionary
            indices = dict()
            for i in range(0, len(occ)):
                if occ[i] in indices:
                    indices[occ[i]].append(i)
                else:
                    indices[occ[i]] = [i]

            # sort occ
            occ.sort(reverse = True)

            # read dictionary and add to currProblem class
            for i in range(0, len(occ)):
                currIndex = indices[occ[i]].pop();
                currProblem.occ.append(currIndex)

            # append the completed problem and clear occ
            occ.clear()
            problemList.append(currProblem)

            # begin the new problem
            celems = currLine.split(" ")
            currProblem = Problem(int(celems[1]), int(celems[2]), 0, -1, celems[3])

        # if starts with p, set all other class elements
        elif currLine[0] == 'p':

            pelems = currLine.split(" ")
            currProblem.numVariables = int(pelems[2])
            currProblem.numClauses = int(pelems[3])
            occ = [0] * currProblem.numVariables
    
        # otherwise, append equation to current problem
        else: 

            eq = currLine.split(",")

            # convert chars to int and add to occ
            for i in range(0, len(eq)):
                eq[i] = int(eq[i])
                if eq[i] != 0:
                    occ[abs(eq[i])-1] += 1

            currProblem.probArray.append(eq)

        # read next line
        currLine = rFile.readline().strip()

    # append last problem to list
    problemList.append(currProblem)

    return problemList



# returns an array of the next assignments to try, AND a value if it is unsatisfiable or not
# currProblem is a problem object
# prevProblemRes is an integer representing what the last verifyWFF outputted
# currStack is the current stack of vars that we were using
def getAssignments(currProblem, prevProblemRes, currStack):

    # if prevProblemRes is 10, then this is the initializer
    if prevProblemRes == 10:

        # initialize stack and assignments
        # do the first relative variable in currProblem's occ
        firstVar = Var(currProblem.occ[0]+1, 0)
        currStack.append(firstVar)

    # prevProblem is undetermined - ADD TO STACK
    elif prevProblemRes == -1:

        # create new variable
        # use the next available variable in occ
        newVar = Var(currProblem.occ[len(currStack)]+1, 0)

        # add to stack
        currStack.append(newVar)

    # prevProblem is unsatisfiable - SWITCH VALUE OR POP
    elif prevProblemRes == 0:

        # first try switching value at the top
        if currStack[-1].allValsTried == False:

            currStack[-1].swapVal()

        # if not that, try popping until we get to a value we can switch
        else:
            
            # loop until valid var is found or stack is empty
            while True:

                currStack.pop()

                # if stack is empty, then problem is unsatisfiable
                if len(currStack) <= 0:
                    return [], 0

                # test if we can switch top value
                if currStack[-1].allValsTried == False:
                    
                    # switch var value
                    currStack[-1].swapVal()
                    break

    # We have found that the problem is satisfiable
    else:
        return [], 1
                    
    # create and return assignments vector
    assignments = [-1] * currProblem.numVariables
    for elem in currStack:
        assignments[elem.relativeVar-1] = elem.currVal

    return assignments, -1



# Takes a problem and evaluates if it is satisfiable or not
# currProblem is a problem object
# assignments is an array of integers representing the current variable assignments
    # 0 is false, 1 is true, -1 is UNDETERMINED
# returns a 0 if WFF is unsatisfiable, returns a 1 if satisfiable, returns -1 if undetermined
def verifyWFF(currProblem, assignments):

    # loop through the prob array of current problem
    for clause in currProblem.probArray:

        # represents the return value of the clause: 0 is false, 1 is true, -1 is undetermined
        clauseRet = -1

        # represents if we had an undetermined var in our clause
        hasUndetermined = False

        # loop through clause until we hit a true var OR zero
        for literal in clause:

            # base case: 0
            if literal == 0:
                break

            # get absolute value and negation
            val = abs(literal)
            negation = (literal < 0)

            # if assignments at this value is -1, then don't test it
            if (assignments[val-1] == -1):
                hasUndetermined = True
                continue

            # test if this value is true
            if negation:
                if assignments[val-1] == 0:
                    clauseRet = True
                    break

            else:
                if assignments[val-1] == 1:
                    clauseRet = True
                    break

        # if clause ret is still -1 and there were no undetermineds, then its unsatisfiable
        if clauseRet == -1 and hasUndetermined == False:
            return 0

        # if clause ret is still -1, then we have an undetermined clause
        if clauseRet == -1:
            return -1

    # if we got through every clause, then it is satisfiable
    return 1



# This function prints the result of our current problem solver
# currProblem is a Problem object
# result is a boolean value representing if the problem was satisfiable or not
# return if the the two evaluations agreed
def writeOutput(currProblem, result):

    print("------------------------------------------")
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

    totalTime = 0

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

        # initialize stack and assignments
        stack = list()
        assignments, res = getAssignments(problem, 10, stack)

        # loop through possible assignments
        while True:

            test = verifyWFF(problem, assignments)
            assignments, res = getAssignments(problem, test, stack)

            # If res is 1 or 0, then we have a result
            if res == 1:
                problemRes = True
                break

            if res == 0:
                break

        # end the timer and add to array
        endTime = time.time()
        probTimes.append((endTime - startTime)*(10**6))
        totalTime += (endTime - startTime)*(10**6)

        # if output not supressed, print results
        if suppressOutput == False:
            test = writeOutput(problem, problemRes)

    print("Total time was", totalTime/(10**6)/60, "minutes")



main()
