def run(intcode):

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
            intcode[position] = 1
            index += 2
        if (mode == "04"):
            output = intcode[index + 1] if is_immediate_mode3 else intcode[intcode[index + 1]] 
            index += 2

    return output

def Puzzle1(intcode):    
    return run(intcode)

if __name__ == "__main__":
    input = open("input.txt", "r")
    numbers = [int(x) for x in input.readline().split(",")]
    print("Puzzle 1: " + str(Puzzle1(numbers)))