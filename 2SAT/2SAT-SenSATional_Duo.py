import sys
import time



# Class "problem"
class Problem:

    def __init__(self, probNumber_in, maxLiterals_in, numVariables_in, numClauses_in, answer_in):
        self.probNumber = int(probNumber_in)
        self.maxLiterals = int(maxLiterals_in)
        self.numVariables = int(numVariables_in)
        self.numClauses = int(numClauses_in)
        self.totalLiterals = 0
        self.execTime = 0
        self.answer = answer_in
        self.myAnswer = '?'
        self.probArray = list()



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

# a set to keep track of the variables that already exist in the stack
vars_in_stack = set()

# initialize overall file variables
numSat = 0
numUnsat = 0
numAnsProv = 0
numCorrect = 0

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

            if (celems[3] != '?'):
                numAnsProv += 1
            
        # if starts with p, set all other class elements
        elif currLine[0] == 'p':

            pelems = currLine.split(" ")
            currProblem.numVariables = int(pelems[2])
            currProblem.numClauses = int(pelems[3])
    
        # otherwise, append equation to current problem
        else: 

            eq = currLine.split(",")
            for i in range(0, len(eq)):
                # convert char to int
                eq[i] = int(eq[i])
                if (eq[i] != 0):
                    currProblem.totalLiterals += 1

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
def getAssignments(currProblem, prevProblemRes, currStack, bonusAssigns):

    # if prevProblemRes is 10, then this is the initializer
    if prevProblemRes == 10:

        # initialize stack and assignments
        firstVar = Var(1, 0)
        currStack.append(firstVar)
        vars_in_stack.add(1)

    # prevProblem is undetermined - ADD TO STACK
    elif prevProblemRes == -1:
        assignmentMade = False
        
        # add bonus assigns for 2sat
        for assignment in bonusAssigns.items():
            if not assignment[0] in vars_in_stack:
                assignmentMade = True
                newVar = Var(assignment[0], assignment[1])
                newVar.valsTried = [0,1]
                newVar.allValsTried = True
                currStack.append(newVar)
                vars_in_stack.add(assignment[0])

        if not assignmentMade:
            # create new variable
            assign_var = 0
            for i in range(1, currProblem.numVariables + 1): 
                if not i in vars_in_stack:
                    assign_var = i
                    break
            # if no assignments left, declare problem unsatisfiable
            if assign_var == 0:
                return [], 0

            newVar = Var(assign_var, 0)

            # add to stack
            currStack.append(newVar)
            vars_in_stack.add(assign_var)

    # prevProblem is unsatisfiable - SWITCH VALUE OR POP
    elif prevProblemRes == 0:

        # first try switching value at the top
        if currStack[-1].allValsTried == False:

            currStack[-1].swapVal()

        # if not that, try popping until we get to a value we can switch
        else:
            
            # loop until valid var is found or stack is empty
            while True:

                x = currStack.pop()
                vars_in_stack.remove(x.relativeVar)

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

    # dictionary that stores {variable: value} pairs to be appended that must be true
    bonusAssigns = {}

    # loop through the prob array of current problem
    for clause in currProblem.probArray:

        # represents the return value of the clause: 0 is false, 1 is true, -1 is undetermined
        clauseRet = -1

        # represents if we had an undetermined var in our clause
        hasUndetermined = False

        # loop through clause until we hit a true var OR zero
        for literal in clause:

            # EOL character: 0
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
            return [], 0

        # if clause ret is still -1, then we have an undetermined clause
        if clauseRet == -1:

            # check for 2sat algorithm opportunity
            for clause in currProblem.probArray:
                if (assignments[abs(clause[0])-1] == 0 and clause[0] > 0) or (assignments[abs(clause[0])-1] == 1 and clause[0] < 0):
                    assign_var = abs(clause[1])
                    assign_val = 1 if (clause[1] > 0) else 0
                elif (assignments[abs(clause[1])-1] == 0 and clause[1] > 0) or (assignments[abs(clause[1])-1] == 1 and clause[1] < 0):
                    assign_var = abs(clause[0])
                    assign_val = 1 if (clause[0] > 0) else 0
                else:
                    continue

                if assign_var in bonusAssigns:
                    # if duplicate contradicts, then assignment is unsatisfiable
                    if bonusAssigns[assign_var] != assign_val:
                        return [], 0
                else:
                    bonusAssigns[assign_var] = assign_val
                    
            return bonusAssigns, -1

    # if we got through every clause, then it is satisfiable
    return [], 1



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
        global numCorrect
        numCorrect += 1
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

    csvFile = open("res2SAT.csv", "w")

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
        vars_in_stack.clear()
        assignments, res = getAssignments(problem, 10, stack, [])

        # loop through possible assignments
        while True:

            bonusAssigns, test = verifyWFF(problem, assignments)
            assignments, res = getAssignments(problem, test, stack, bonusAssigns)

            # If res is 1 or 0, then we have a result
            if res == 1:
                global numSat
                numSat += 1
                problemRes = True
                break

            if res == 0:
                global numUnsat
                numUnsat += 1
                break

        # end the timer and add to array
        endTime = time.time()
        probTimes.append((endTime - startTime)*(10**6))
        totalTime += (endTime - startTime)*(10**6)

        # add to exec time
        problem.execTime = (endTime - startTime)*(10**6)

        # if output not supressed, print results
        if suppressOutput == False:
            test = writeOutput(problem, problemRes)

        # write to csv file
        csvFile.write(str(problem.probNumber) + ",")
        csvFile.write(str(problem.numVariables) + ",")
        csvFile.write(str(problem.numClauses) + ",")
        csvFile.write(str(problem.maxLiterals) + ",")
        csvFile.write(str(problem.totalLiterals) + ",")
        csvFile.write(str(problem.myAnswer) + ",")
        csvFile.write("0,")
        csvFile.write(str(problem.execTime) + "\n")

    print("total time: " + str(totalTime) + "\n")

    # write end of file
    csvFile.write("2SAT,")
    csvFile.write("The SenSATional Duo,")
    csvFile.write(str(len(probList)) + ",")
    csvFile.write(str(numSat) + ",")
    csvFile.write(str(numUnsat) + ",")
    csvFile.write(str(numAnsProv) + ",")
    csvFile.write(str(numCorrect))

    csvFile.close()

main()
