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
        self.predAnswer = predAnswer_in
        self.answer = '?'

    # function that returns if a problem is satisfied given the variables
    # assignments is an array of integers to represent the current variables assignments
    # returns a boolean value: true if it is satisfiable, false if not
    def verifyWFF(self, assignments):

        # loop through the prob array of current problem
        for clause in self.probArray:

            # represents the return value of clause
            clauseRet = False

            # loop through the clause until a zero is hit
            for literal in clause:
                
                if literal == 0:
                    break

                # get absolute value and negation
                val = abs(literal)
                negation = (literal < 0)

                # test if this literal evaluates to true, if it is then break
                if negation:
                    if assignments[val-1] == 0:
                        clauseRet = True
                        break
                    
                else:
                    if assignments[val-1] == 1:
                        clauseRet = True
                        break

            # if clause_ret is still false, then it is unsatisfiable with these assignments
            if clauseRet == False:
                return False

        # if got through every clause, then return true
        return True

    # This function prints the result of our current problem solver
    def writeOutput(self):

        print("-----------------------------------------")
        print("Analyzing problem " + str(self.probNumber) + "...")

        if self.answer == 'U':
            print("Problem " + str(self.probNumber) + " evaluated to be UNSATISFIABLE")
        elif self.answer == 'S':
            print("Problem " + str(self.probNumber) + " evaluated to be SATISFIABLE")
        else:
            print("Problem " + str(self.probNumber) + " is UNDETERMINED")

        # Check against answer in currProblem
        if self.predAnswer == self.answer:
            print("This evaluation is CORRECT\n")
        elif self.predAnswer == '?':
            print("")
        else:
            print("This evaluation is INCORRECT\n")

        return

    def recordStats(self, wFile, assignments):
        
        wFile.write(str(self.probNumber) + ",")
        wFile.write(str(self.numVariables) + ",")
        wFile.write(str(self.numClauses) + ",")
        wFile.write(str(self.maxLiterals) + ",")
        wFile.write(str(self.totalLiterals) + ",")
        wFile.write(self.answer + ",")

        # print if prediction matched
        if (self.predAnswer == '?'):
            wFile.write("0,")
        elif (self.predAnswer == self.answer):
            wFile.write("1,")
        else:
            wFile.write("-1,")

        wFile.write(str(round(self.execTime)))

        # print the working assignments, if needed
        if (self.answer == 'S'):
            wFile.write(",")
            for i in range(0, len(assignments)-1):
                wFile.write(str(assignments[i]) + ",")
            wFile.write(str(assignments[len(assignments) - 1]))

        wFile.write("\n")

        return



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
        if celems[3] == 'U' or celems[3] == 'S':
            self.numAnswersProvided += 1

        # Loop through file
        currLine = rFile.readline().strip()
        while(currLine):

            # if current line starts with c, begin a new Problem
            if currLine[0] == 'c':
           
                self.probList.append(currProblem)
                celems = currLine.split(" ")
                currProblem = Problem(int(celems[1]), int(celems[2]), -1, -1, celems[3])
                self.numProblems += 1
                if celems[3] == 'U' or celems[3] == 'S':
                    self.numAnswersProvided += 1

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
                currProblem.totalLiterals += len(eq) - 1

            # read next line
            currLine = rFile.readline().strip()

        # append last problem to list
        self.probList.append(currProblem)

        return

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

    # Open CSV file
    csvFile = open("resBactrack.csv", "w")

    # Get file stats
    fstats = ProblemFile()
    fstats.getProblems(filename)

    # loop through list to get results
    for currProblem in fstats.probList:
        
        problemRes = False

        # start timer for current problem
        startTime = time.time()

        # get each assignment
        for i in range(0, 2**currProblem.numVariables):

            # test assignment
            assignment = generateAssignment(currProblem, i)
            assignmentRes = currProblem.verifyWFF(assignment)

            # if true, then it is satisfiable
            if assignmentRes == True:
                problemRes = True
                break
        
        # end the timer and add problem
        endTime = time.time()
        currProblem.execTime = (endTime - startTime)*(10**6)

        # add problem Res to problem class
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
    
        # Record to CSV file
        currProblem.recordStats(csvFile, assignment)

    # Record overall stats to CSV file
    fstats.printOverallStats(csvFile, filename)



main()
