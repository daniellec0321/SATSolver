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

    probList = list()

    # initialize class loop
    celems = equation_list[0].split(" ")
    pelems = equation_list[1].split(" ")

    init = Problem(int(celems[1]), int(celems[2]), int(pelems[2]), int(pelems[3]), celems[3])

    # loop through list and parse
    counter = 0
    while counter < len(equation_list):

        celems = equation_list[counter].split(" ")
        counter += 1
        pelems = equation_list[counter].split(" ")
        counter += 1

        init = Problem(int(celems[1]), int(celems[2]), int(pelems[2]), int(pelems[3]), celems[3])

        # read in problem array
        while counter < counter+init.numClauses:

            app_clause = list()

            # get clause
            clause_in = equation_list[counter].split(",")
            counter += 1

            # append everything to clause, EXCEPT FOR ZERO
            for i in range(0, len(clause_in)-1):
                app_clause.append(int(clause_in[i]))

            # If length of clause is less than the maxLiterals + 1, append with zeros
            if len(clause_in) < init.maxLiterals + 1:
                for i in range(len(clause_in), init.maxLiterals+1):
                    app_clause.append(0)

            # append to current problem class
            init.probArray.append(app_clause)

        # append class problem to list
        probList.append(init)

    return probList



# initialize brute force
equation_list, numProblems = readFile("../tests/kSAT.txt")
probList = getProblems(equation_list, numProblems)

# c, problem number, max literals in a clause, answer
# p, cnf, number of variables, number of clauses
