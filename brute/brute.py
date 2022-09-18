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
def getProblems(equation_list):

    problemList = list()

    # initialize readings
    celems = equation_list[0].split(" ")
    pelems = equation_list[1].split(" ")
    currProblem = Problem(celems[1], celems[2], pelems[2], pelems[3], celems[3])

    for counter in range(2, len(equation_list)):

        # if equation list at counter starts with c, reset
        if equation_list[counter][0] == 'c':
           
            problemList.append(currProblem)
            celems = equation_list[counter].split(" ")
            currProblem = Problem(int(celems[1]), int(celems[2]), -1, -1, celems[3])

        # if starts with p, set all other class elements
        elif equation_list[counter][0] == 'p':

            pelems = equation_list[counter].split(" ")
            currProblem.numVariables = int(pelems[2])
            currProblem.numClauses = int(pelems[3])

        else: 

            # append equation to list
            eq = equation_list[counter].split(",")
            for i in range(0, len(eq)):
                eq[i] = int(eq[i])
            currProblem.probArray.append(eq)

    # append last problem to list
    problemList.append(currProblem)

    return problemList
