import copy

relative_base = 0

def get_index(intcode, index, mode):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base

def run(intcode, input):
    global relative_base

    # Puzzle vars   
    input_index = 0

    # Intcode vars
    output = 0
    index = 0
    while(intcode[index] != 99):
        instruction = str(intcode[index]).zfill(2)

        mode = instruction[-2:]
        operand1_mode = instruction[len(instruction) - 3] if len(instruction) > 2 else '0'
        operand2_mode = instruction[len(instruction) - 4] if len(instruction) > 3 else '0'
        operand3_mode = instruction[len(instruction) - 5] if len(instruction) > 4 else '0'

        index1 = get_index(intcode, index + 1, operand1_mode)
        index2 = get_index(intcode, index + 2, operand2_mode)
        index3 = get_index(intcode, index + 3, operand3_mode)

        operand1 = intcode[index1] if index1 in intcode else 0
        operand2 = intcode[index2] if index2 in intcode else 0

        if (mode == "01"):
            intcode[index3] = operand1 + operand2
            index += 4
        if (mode == "02"):
            intcode[index3] = operand1 * operand2
            index += 4
        if (mode == "03"):
            intcode[index1] = input[input_index]
            input_index += 1
            index += 2
        if (mode == "04"):
            output = operand1
            if output > 255:
                return output
            index += 2
        if (mode == "05"):
            index = operand2 if operand1 != 0 else index + 3
        if (mode == "06"):
            index = operand2 if operand1 == 0 else index + 3 
        if (mode == "07"):
            intcode[index3] = 1 if operand1 < operand2 else 0
            index += 4
        if (mode == "08"):
            intcode[index3] = 1 if operand1 == operand2 else 0
            index += 4
        if (mode == "09"):
            relative_base += operand1
            index += 2
    
    return output
    
def Puzzle1(intcode):
    '''
    A = 65, B = 66, C = 67, D = 68, J = 74, T = 84, O = 79, R = 82 
    1. NOT A J
    2. NOT B T
    3. OR T J
    4. NOT C T
    5. OR T J
    6. NOT D T
    7. NOT T T
    8. AND T J
    9. WALK
    '''
    input = [78,79,84,32,65,32,74,10,   
             78,79,84,32,66,32,84,10,   
             79,82,32,84,32,74,10,   
             78,79,84,32,67,32,84,10,
             79,82,32,84,32,74,10,
             78,79,84,32,68,32,84,10,
             78,79,84,32,84,32,84,10,
             65,78,68,32,84,32,74,10,   
             87,65,76,75,10] 
    return run(intcode, input)

def Puzzle2(intcode):
    '''
    A = 65, B = 66, C = 67, D = 68, J = 74, T = 84, O = 79, R = 82 
    1. NOT A J
    2. NOT B T
    3. OR T J
    4. NOT C T
    5. OR T J
    6. NOT D T
    7. NOT T T
    8. AND T J (if one of the next three tiles is a hole and the 4th is solid, jump)

    9. NOT H T
    10. NOT T T
    11. OR E T
    12. AND T J (but only if also either the 5th or the 9th tile are solid)

    11. RUN
    '''
    input = [78,79,84,32,65,32,74,10,  #NOT 
             78,79,84,32,66,32,84,10,  #NOT
             79,82,32,84,32,74,10,     #OR
             78,79,84,32,67,32,84,10,  #NOT
             79,82,32,84,32,74,10,     #OR
             78,79,84,32,68,32,84,10,  #NOT
             78,79,84,32,84,32,84,10,  #NOT
             65,78,68,32,84,32,74,10,  #AND

             78,79,84,32,72,32,84,10,  #NOT
             78,79,84,32,84,32,84,10,  #NOT
             79,82,32,69,32,84,10,     #OR
             65,78,68,32,84,32,74,10,

             82,85,78,10] 
    return run(intcode, input)

if __name__ == "__main__":
    input = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(input.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)
    print("Puzzle 1: " + str(Puzzle1(intcode)))
    print("Puzzle 2: " + str(Puzzle2(intcodeCopy)))
