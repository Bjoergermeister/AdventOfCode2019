import copy

relative_base = 0
field_width = 45
field_height = 41

def get_index(intcode, index, mode):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base

def run(intcode, movement_commands):
    global relative_base
    relative_base = 0

    # Puzzle vars
    field = []
    movement_command_index = 0

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
        elif (mode == "02"):
            intcode[index3] = operand1 * operand2
            index += 4
        elif (mode == "03"):
            intcode[index1] = movement_commands[movement_command_index]
            movement_command_index += 1
            index += 2
        elif (mode == "04"):
            output = operand1

            if len(movement_commands) > 0: # This is puzzle 2
                if output > 255:
                    return output
            elif output != 10: # This is puzzle 1
                field.append(chr(output))
            index += 2
        elif (mode == "05"):
            index = operand2 if operand1 != 0 else index + 3
        elif (mode == "06"):
            index = operand2 if operand1 == 0 else index + 3 
        elif (mode == "07"):
            intcode[index3] = 1 if operand1 < operand2 else 0
            index += 4
        elif (mode == "08"):
            intcode[index3] = 1 if operand1 == operand2 else 0
            index += 4
        else:
            relative_base += operand1
            index += 2

    return field

def is_intersection(field, position):
    global field_width

    # If the position if at one of the edges, it can't be an intersection, so first check for that
    if position < field_width or position > len(field) - field_width or position % field_width == 0 or position % field_width == 44:
        return False
    top = field[position - field_width] == '#'
    bottom = field[position + field_width] == '#'
    left = field[position - 1] == '#'
    right = field[position + 1] == '#'
    return top and bottom and left and right

def Puzzle1(intcode):    
    global field_width
    global field_height

    field = run(intcode, [])    
    
    alignment_parameters = 0
    for j in range(0, field_height):
        for i in range(0, field_width):
            array_pos = j * field_width + i
            if field[array_pos] == '#':
                if is_intersection(field, array_pos):     
                    x = array_pos % field_width
                    y = array_pos // field_width
                    alignment_parameters += x * y
    return alignment_parameters

def Puzzle2(intcode):
    intcode[0] = 2
    '''
    Main: A,B,A,C,B,A,C,B,A,C
    A: L6,L4,R12
    B: L6,R12,R12,L8
    C: L6,L10,L10,L6
    
    ASCII-Codes: 65='A', 66='B', 67='C', 44=',', 10='\n', 76='L', 82='R'
    '''
    main = [65,44,66,44,65,44,67,44,66,44,65,44,67,44,66,44,65,44,67,10]
    a = [76,44,54,44,76,44,52,44,82,44,49,50,10]
    b = [76,44,54,44,82,44,49,50,44,82,44,49,50,44,76,44,56,10]
    c = [76,44,54,44,76,44,49,48,44,76,44,49,48,44,76,44,54,10]
    movement_commands = main
    movement_commands.extend(a)
    movement_commands.extend(b)
    movement_commands.extend(c)   
    movement_commands.extend([110,10]) # No Video feed 
    return run(intcode, movement_commands)

if __name__ == "__main__":
    file = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(file.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)
    print("Puzzle 1: " + str(Puzzle1(intcode)))
    print("Puzzle 2: " + str(Puzzle2(intcodeCopy)))