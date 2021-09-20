def Puzzle1(intcode):    
    
    intcode[1] = 12
    intcode[2] = 2

    index = 0
    while intcode[index] != 99:
        operand1 = intcode[intcode[index + 1]]
        operand2 = intcode[intcode[index + 2]]
        intcode[intcode[index + 3]] = operand1 + operand2 if intcode[index] == 1 else operand1 * operand2

    return intcode[0]

if __name__ == "__main__":
    inputFile = open("input.txt", "r")
    input = inputFile.readline()
    intcode = [int(x) for x in input.split(",")]

    print("Puzzle 1: " + str(Puzzle1(intcode)))