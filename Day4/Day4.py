min = 347312
max = 805915

def checkRules(numbers, checkGroups: bool) -> bool:
    adjacent = False
    for i in range(len(numbers) - 1):
        if (numbers[i] > numbers[i + 1]):
            for j in range(i + 1, len(numbers)):
                numbers[j] = numbers[i]
            numbers[len(numbers)-1] = numbers[len(numbers)-1] - 1
            return False

        if (numbers[i] == numbers[i + 1]):
            if (checkGroups is True and adjacent is False):
                checkBehind = (i < len(numbers) - 2 and numbers[i] == numbers[i + 2])
                checkBefore = (i > 0 and numbers[i] == numbers[i - 1])
                if (checkBefore is True or checkBehind is True):
                    continue

            adjacent = True

    return adjacent

def Puzzle1() -> str:
    current = min

    validNumbers = 0
    while current <= max: 
        numbers = [int(x) for x in str(current)]
        if (checkRules(numbers, False)):        
            validNumbers = validNumbers + 1

        current = int("".join([str(x) for x in numbers])) + 1
    return str(validNumbers)

def Puzzle2():
    current = min
    validNumbers = 0
    while current <= max: 
        numbers = [int(x) for x in str(current)]
        if (checkRules(numbers, True)):      
            validNumbers = validNumbers + 1

        current = int("".join([str(x) for x in numbers])) + 1
    return str(validNumbers)


if __name__ == "__main__":
    print("Puzzle 1: " + Puzzle1())
    print("Puzzle 2: " + Puzzle2())