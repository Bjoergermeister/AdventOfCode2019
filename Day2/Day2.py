import copy

def run(intcode):
    index = 0
    while intcode[index] != 99:
        operand1 = intcode[intcode[index + 1]]
        operand2 = intcode[intcode[index + 2]]
        
        if (intcode[index + 3] >= len(intcode)): 
            return -1

        intcode[intcode[index + 3]] = operand1 + operand2 if intcode[index] == 1 else operand1 * operand2
        index += 4

    return intcode[0]

def Puzzle1(intcode):    
    
    intcode[1] = 12
    intcode[2] = 2

    return run(intcode)

def Puzzle2(intcode):

    for i in range(100):
        for j in range(100):            
            intcodeCopy = copy.deepcopy(intcode)
            intcodeCopy[1] = i
            intcodeCopy[2] = j

            if (run(intcodeCopy) == 19690720):
                return 100 * i + j

if __name__ == "__main__":
    inputFile = open("input.txt", "r")
    input = inputFile.readline()
    intcode = [int(x) for x in input.split(",")]

    print("Puzzle 1: " + str(Puzzle1(intcode)))
    
    intcode = [int(x) for x in input.split(",")]
    print("Puzzle 2: " + str(Puzzle2(intcode)))