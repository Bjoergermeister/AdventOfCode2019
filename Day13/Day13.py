import copy

relative_base = 0

def get_index(intcode, index, mode):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base

def run(intcode):
    global relative_base

    # Puzzle vars
    output_counter = 0
    block_tile_count = 0
    score = 0
    x = None
    y = None
    ball_position = None
    paddle_position = None
    joystick = 0

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
            intcode[index1] = joystick
            index += 2
        if (mode == "04"):
            output = operand1
            if output_counter == 0:
                x = output
                output_counter += 1
            elif output_counter == 1:
                y = output
                output_counter += 1
            else:
                output_counter = 0
                if x == -1:
                    score = output
                elif output == 2:
                    block_tile_count += 1
                elif output == 3:
                    paddle_position = (x, y)
                elif output == 4:
                    ball_position = (x, y)
                
                    if paddle_position is not None:
                        if ball_position[0] == paddle_position[0]:
                            joystick = 0
                        elif ball_position[0] < paddle_position[0]:
                            joystick = -1
                        else:
                            joystick = 1
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
    
    return block_tile_count, score

def Puzzle1(intcode):
    block_tile_count, score = run(intcode)
    return block_tile_count

def Puzzle2(intcode):
    intcode[0] = 2
    block_tile_count, score = run(intcode)
    return score

if __name__ == "__main__":
    input = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(input.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)
    print("Puzzle 1: " + str(Puzzle1(intcode)))
    print("Puzzle 2: " + str(Puzzle2(intcodeCopy)))