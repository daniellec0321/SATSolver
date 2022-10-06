import sys
import time



# Class "problem"
class Problem:

    def __init__(self, probNumber_in, maxLiterals_in, numVariables_in, numClauses_in, predAnswer_in):
        self.probNumber = int(probNumber_in)
        self.maxLiterals = int(maxLiterals_in)
        self.numVariables = int(numVariables_in)
        self.numClauses = int(numClauses_in)
        self.totalLiterals = 0
        self.execTime = 0
        self.probArray = list()
        self.literalOcc = list()
        self.predAnswer = predAnswer_in
        self.answer = '?'

    # Given some external assignments, evaluates if it is satisfiable or not
    # assignments is an array of integers representing the current variable assignments
        # 0 is false, 1 is true, -1 is UNDETERMINED
    # returns a 0 if WFF is unsatisfiable, returns a 1 if satisfiable, returns -1 if undetermined
    def verifyWFF(self, assignments):

        # loop through the prob array of current problem
        for clause in self.probArray:

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

                # if value is true, then the whole clause evaluates to true
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

            # otherwise, if clause ret is still -1, then we have an undetermined clause
            elif clauseRet == -1 and hasUndetermined == True:
                return -1

        # if we got through every clause, then it is satisfiable
        return 1

    # This function prints the result of our current problem solver to terminal
    def writeOutput(self):

        print("------------------------------------------")
        print("Analyzing problem " + str(self.probNumber) + "...")

        if self.answer == 'U':
            print("Problem " + str(self.probNumber) + " evaluated to be UNSATISFIABLE")
        elif self.answer == 'S':
            print("Problem " + str(self.probNumber) + " evaluated to be SATISFIABLE")
        else:
            print("Problem remains UNDETERMINED\n")
            return

        # Check against predicted answer
        if (self.predAnswer == self.answer):
            print("This evaluation is CORRECT\n")
            return
        elif (self.predAnswer == '?'):
            print("")
            return
        else:
            print("This evaluation is INCORRECT\n")
            return

    # Records stats of problem into CSV file
    def recordStats(self, wFile, assignments):

        wFile.write(str(self.probNumber) + ",")
        wFile.write(str(self.numVariables) + ",")
        wFile.write(str(self.numClauses) + ",")
        wFile.write(str(self.maxLiterals) + ",")
        wFile.write(str(self.totalLiterals) + ",")
        wFile.write(self.answer + ",")

        # print if prediction was matched
        if (self.predAnswer == '?'):
            wFile.write("0,")
        elif (self.predAnswer == self.answer):
            wFile.write("1,")
        else:
            wFile.write("-1,")

        wFile.write(str(round(self.execTime)))

        # Print the working assignments, if needed
        if (self.answer == 'S'):
            wFile.write(",")
            for i in range(0, len(assignments) - 1):
                wFile.write(str(assignments[i]) + ",")
            wFile.write(str(assignments[len(assignments) - 1]))

        wFile.write("\n")

        return



# Class "variable" (holds a current variable value and its flags)
# vals will always be 0 or 1
class Var:

    def __init__(self, relativeVar, currVal):
        self.relativeVar = relativeVar
        self.currVal = currVal
        self.valsTried = [currVal]
        self.allValsTried = False

    # Changes the current value from 0 to 1 or 1 to 0
    def swapVal(self):
        self.currVal = (self.currVal + 1) % 2
        self.valsTried.append(self.currVal)
        if len(self.valsTried) >= 2:
            self.allValsTried = True



# Holds the information for a file of WFFs
class ProblemFile:

    def __init__(self):
        self.numProblems = 0
        self.numUnsatisfiable = 0
        self.numSatisfiable = 0
        self.numAnswersProvided = 0
        self.numAnsweredCorrectly = 0
        self.probList = list()

    # parse a list into LIST OF CLASS PROBLEMS
    # filename is a string that contains path to file
    def getProblems(self, filename):

        rFile = open(filename, "r")

        # initialize readings
        celems = rFile.readline().strip().split(" ")
        pelems = rFile.readline().strip().split(" ")
        currProblem = Problem(celems[1], celems[2], pelems[2], pelems[3], celems[3])
        self.numProblems += 1
        if (celems[3] == 'U') or (celems[3] == 'S'):
            self.numAnswersProvided += 1

        # initialize list to count occurrences of each variables
        occ = [0] * currProblem.numVariables

        # Loop through file
        currLine = rFile.readline().strip()
        while(currLine):

            # if current line starts with c, begin a new Problem
            if currLine[0] == 'c':

                # Use a dictionary to match the number of occurrences with its index
                # Key: number of occurrences, Value: Relative literal
                indices = dict()
                for i in range(0, len(occ)):
                    if occ[i] in indices:
                        indices[occ[i]].append(i)
                    else:
                        indices[occ[i]] = [i]

                # Sort occ from highest to lowest
                occ.sort(reverse = True)

                # Read dictionary, create a list of the literals where it is ordered from most common literal to least common literal
                for i in range(0, len(occ)):
                    currIndex = indices[occ[i]].pop();
                    currProblem.literalOcc.append(currIndex)

                # append the completed problem and clear occ
                occ.clear()
                self.probList.append(currProblem)

                # begin the new problem
                celems = currLine.split(" ")
                currProblem = Problem(int(celems[1]), int(celems[2]), 0, -1, celems[3])
                self.numProblems += 1
                if (celems[3] == 'U') or (celems[3] == 'S'):
                    self.numAnswersProvided += 1

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

                # add equation and num variables to problem
                currProblem.probArray.append(eq)
                currProblem.totalLiterals += len(eq) - 1

            # read next line
            currLine = rFile.readline().strip()

        # Finish up the final problem
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
            currIndex = indices[occ[i]].pop()
            currProblem.literalOcc.append(currIndex)

        self.probList.append(currProblem)

        return

    # prints stats of file into CSV
    def printOverallStats(self, wFile, filename):

        arr = filename.split(".cnf")
        filename = arr[0]
        arr = filename.split("../tests/")
        noExt = arr[1]

        wFile.write(noExt + ",")
        wFile.write("The SenSATional Duo,")
        wFile.write(str(self.numProblems) + ",")
        wFile.write(str(self.numSatisfiable) + ",")
        wFile.write(str(self.numUnsatisfiable) + ",")
        wFile.write(str(self.numAnswersProvided) + ",")
        wFile.write(str(self.numAnsweredCorrectly))



# EXTERNAL FUNCTION, NOT PART OF A CLASS
# returns an array of the next assignments to try, AND a value if it is unsatisfiable or not
# currProblem is a problem object
# prevProblemRes is an integer representing what the last verifyWFF outputted
# currStack is the current stack of vars that we were using
def getAssignments(currProblem, prevProblemRes, currStack):

    # if prevProblemRes is 10, then this is the initializer
    if prevProblemRes == 10:

        # initialize stack and assignments
        # do the first relative variable in currProblem's occ
        firstVar = Var(currProblem.literalOcc[0]+1, 0)
        currStack.append(firstVar)

    # prevProblem is undetermined - ADD TO STACK
    elif prevProblemRes == -1:

        # create new variable
        # use the next available variable in occ
        newVar = Var(currProblem.literalOcc[len(currStack)]+1, 0)
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

        # create and return assignments vector that gave us a satisfiable answer
        assignments = [-1] * currProblem.numVariables
        for elem in currStack:
            assignments[elem.relativeVar-1] = elem.currVal

        return assignments, 1
                    
    # create and return assignments vector
    assignments = [-1] * currProblem.numVariables
    for elem in currStack:
        assignments[elem.relativeVar-1] = elem.currVal

    return assignments, -1



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

    # open file to record csv file
    csvFile = open("resBacktrack.csv", "w")
    
    # records stats about the file
    fstats = ProblemFile()

    # get problem list
    fstats.getProblems(filename)

    # loop through list to get results
    for currProblem in fstats.probList:

        problemRes = False

        # start timer for current problem
        startTime = time.time()

        # initialize stack and assignments
        stack = list()
        assignments, res = getAssignments(currProblem, 10, stack)

        # loop through possible assignments
        while True:

            res = currProblem.verifyWFF(assignments)
            assignments, res = getAssignments(currProblem, res, stack)

            # If res is 1 or 0, then we have a result
            if res == 1:
                problemRes = True
                break

            if res == 0:
                break

        endTime = time.time()

        # add time taken to problem
        currProblem.execTime = (endTime - startTime)*(10**6)

        # add result to problem
        if problemRes == True:
            currProblem.answer = 'S'
            fstats.numSatisfiable += 1
        else:
            currProblem.answer = 'U'
            fstats.numUnsatisfiable += 1

        # add correctness
        if currProblem.predAnswer == 'U' or currProblem.predAnswer == 'S':
            if currProblem.predAnswer == currProblem.answer:
                fstats.numAnsweredCorrectly += 1

        # if output not supressed, print results
        if suppressOutput == False:
            currProblem.writeOutput()
        
        # Record stats into CSV file
        currProblem.recordStats(csvFile, assignments)

    # Print overall stats
    fstats.printOverallStats(csvFile, filename)
    csvFile.close()



# Execute main
main()
