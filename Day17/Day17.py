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

def run(intcode):
    global relative_base

    # Puzzle vars
    field = []

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
            intcode[index1] = 0
            index += 2
        elif (mode == "04"):
            output = operand1
            if output != 10:
                character = '#' if output == 35 else '.'
                field.append(character)
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

    field = run(intcode)    
    
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

if __name__ == "__main__":
    file = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(file.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)
    print("Puzzle 1: " + str(Puzzle1(intcode)))