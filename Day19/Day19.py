import copy
from math import floor

relative_base = 0
line_endings = []
line_beginnings = []
beam_starting_point = 0

def get_index(intcode, index, mode):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base

def run(intcode, x, y):
    global relative_base

    # Puzzle vars
    is_x_input = True

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
            intcode[index1] = x if is_x_input else y
            is_x_input = False
            index += 2
        if (mode == "04"):
            output = operand1   
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
    global line_endings, line_beginnings, beam_starting_point
    previous = None
    is_first = True
    sum = 0
    for y in range(0, 50):   
        for x in range(0, 50):
            result = run(copy.deepcopy(intcode), x, y)

            if result == 1 and y > 0 and is_first:
                beam_starting_point = (x,y)
                is_first = False
            if previous == 0 and result == 1:
                line_beginnings.append(x)
            elif previous == 1 and result == 0 and y > 0:
                line_endings.append(x - 1)
            previous = result
            sum += result
    return sum

def calculate_drift(line_edges):
    sum = 0
    for i in range(0, len(line_edges) - 1):
        sum += line_edges[i + 1] - line_edges[i]
    return round(sum / (len(line_edges) - 1), 1)

def check_corner(intcode, x, y):
    top_right_corner = 1
    while top_right_corner == 1:        
        top_right_corner = run(copy.deepcopy(intcode), x + 99, y)
        bottom_left_corner = run(copy.deepcopy(intcode), x, y + 99)
        if top_right_corner == 1 and bottom_left_corner == 1:
            return x
        x += 1
    return -1

def Puzzle2(intcode):
    global line_beginnings, line_endings, beam_starting_point

    vertical_drift = calculate_drift(line_beginnings)
    horizontal_drift = calculate_drift(line_endings)
    
    average_horizontal_increase = horizontal_drift - vertical_drift
    vertical_starting_point = beam_starting_point[1] + floor(100 / (average_horizontal_increase))
    horizontal_starting_point = beam_starting_point[0] + floor((vertical_starting_point - beam_starting_point[1]) * vertical_drift)

    x = horizontal_starting_point
    y = vertical_starting_point
    
    # Go right until the beam is met
    while True:
        if run(copy.deepcopy(intcode), x, y) == 1:
            break
        x += 1

    # Find square
    while True:
        result = check_corner(intcode, x, y)
        if result != -1:
            return result * 1000 + y
        y += 1
        while True:
            if run(copy.deepcopy(intcode), x, y) == 1:
                break
            x += 1

if __name__ == "__main__":
    input = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(input.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)
    print("Puzzle 1: " + str(Puzzle1(intcode)))
    print("Puzzle 2: " + str(Puzzle2(intcodeCopy)))
