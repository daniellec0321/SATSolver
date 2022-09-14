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



# parse a list into arrays
def parseFile(equation_list, numProblems):
    return



# main function
# get
test, num = readFile("../tests/kSAT.txt")
print(num)



# c, problem number, max literals in a clause, answer
# p, cnf, number of variables, number of clauses
