import math

def Puzzle1(input):
    totalFuel = 0
    for line in input:
        totalFuel += math.floor(int(line) / 3) - 2

    return totalFuel

if __name__ == "__main__":
    inputFile = open("input.txt", "r")
    input = inputFile.readlines()

    print("Puzzle 1: " + str(Puzzle1(input)))