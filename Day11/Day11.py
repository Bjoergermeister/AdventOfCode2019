relative_base = 0

def turn_robot(current_position, current_direction, turn_direction):

    #Change current_direction
    if turn_direction == 0: # Turn left
        current_direction = current_direction - 1 if current_direction > 0 else 3
    elif turn_direction == 1: # Turn right
        current_direction = current_direction + 1 if current_direction < 3 else 0
    else:
        print("Somethings wrong with the turning: ", turn_direction)

    # Move forward
    x, y = current_position
    if current_direction == 0: # Top
        current_position = (x, y + 1)
    elif current_direction == 1: # Right
        current_position = (x + 1, y)
    elif current_direction == 2: # Bottom
        current_position = (x, y - 1)
    else: # Left
        current_position = (x - 1, y)

    return current_position, current_direction

def get_index(intcode, index, mode):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base

def Puzzle1(intcode):
    global relative_base

    # Puzzle vars
    panels = {}
    is_color_output = True
    current_position = (0, 0)
    current_direction = 0 # 0 = Top, 1 = Right, 2 = Bottom, 3 = Left

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
            intcode[index1] = panels[current_position] if current_position in panels else 0 
            index += 2
        if (mode == "04"):
            output = operand1
            if is_color_output:
                panels[current_position] = output
                is_color_output = False
            else:
                current_position, current_direction = turn_robot(current_position, current_direction, output)
                is_color_output = True
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
    
    return len(panels)

if __name__ == "__main__":
    input = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(input.readline().split(",")):
        intcode[index] = int(number)
    print("Puzzle 1: " + str(Puzzle1(intcode)))