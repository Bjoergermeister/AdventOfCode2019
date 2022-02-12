import copy
  
def run(intcode, input):

    index = 0
    while(intcode[index] != 99):
        instruction = str(intcode[index]).zfill(2)
        
        mode = instruction[-2:]
        is_immediate_mode1 = len(instruction) > 2 and instruction[len(instruction) - 3] == '1'
        is_immediate_mode2 = len(instruction) > 3 and instruction[len(instruction) - 4] == '1'
        is_immediate_mode3 = len(instruction) > 4 and instruction[len(instruction) - 5] == '1'
        
        if (mode == "01"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = operand1 + operand2
            index += 4
        if (mode == "02"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = operand1 * operand2
            index += 4
        if (mode == "03"):
            position = index + 1 if is_immediate_mode3 else intcode[index + 1]
            intcode[position] = input
            index += 2
        if (mode == "04"):
            output = intcode[index + 1] if is_immediate_mode3 else intcode[intcode[index + 1]] 
            index += 2
        if (mode == "05"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            if operand1 != 0:
                index = operand2
            else:
                index += 3
        if (mode == "06"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            if operand1 == 0:
                index = operand2
            else:
                index += 3
        if (mode == "07"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = 1 if operand1 < operand2 else 0
            index += 4
        if (mode == "08"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = 1 if operand1 == operand2 else 0
            index += 4

    return output

def Puzzle1(intcode, input):    
    return run(intcode, input)

def Puzzle2(intcode, input):
    return run(intcode, input)

if __name__ == "__main__":
    input = open("input.txt", "r")
    numbers = [int(x) for x in input.readline().split(",")]
    numbersCopy = copy.deepcopy(numbers)
    print("Puzzle 1: " + str(Puzzle1(numbers, 1)))
    print("Puzzle 2: " + str(Puzzle2(numbersCopy, 5)))
