import copy

relative_base = 0
map = {}
target_position = None

class State:
    def __init__(self, current, direction, distance):
        self.current = current
        self.return_direction = None
        if direction is not None:
            self.return_direction = direction + 1 if direction % 2 == 1 else direction - 1
        self.directions = [x for x in range(1,5) if self.return_direction is None or x != self.return_direction]
        self.direction_index = 0
        self.distance = distance

    def direction(self):
        if self.direction_index >= len(self.directions):
            return self.return_direction
        else:
            return self.directions[self.direction_index]

def get_index(intcode, index, mode):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base

def set_map(position, symbol):
    global map

    if position in map:
        return
    map[position] = symbol

def move(current, direction):
    if direction == 1:
        return (current[0], current[1] + 1)
    if direction == 2:
        return (current[0], current[1] - 1)
    if direction == 3:
        return (current[0] - 1, current[1])
    if direction == 4:
        return (current[0] + 1, current[1])

def run(intcode):
    global relative_base
    global map
    global target_position

    # Puzzle vars
    result = 0
    states = {}
    position = (0,0) 
    current_state = State(position, None, 0)

    # Intcode vars
    output = 0
    index = 0
    while(intcode[index] != 99):
        if current_state.current == (0,0) and current_state.direction_index > 3:
            return result

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
            intcode[index1] = current_state.direction()
            index += 2
        elif (mode == "04"):
            output = operand1
            if output == 0:
                wall_position = move(current_state.current, current_state.direction())
                set_map(wall_position, '#')

                current_state.direction_index += 1                    
            else:                
                symbol = '.' if output == 1 else 'X'
                direction = current_state.direction()
                position = move(position, direction)
                set_map(position, symbol)             
                current_state.direction_index += 1
                if position in states:
                    current_state = states[position]
                else:
                    current_state = State(position, direction, current_state.distance + 1)
                    states[position] = current_state

                # If station is found, return distance from starting position
                if output == 2 and result == 0:
                    result = current_state.distance
                    target_position = position
            
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

def Puzzle1(intcode):
    return run(intcode)

def get_positions(current_position):
    global map

    tuple_add = lambda i, j: (i[0] + j[0], i[1] + j[1])
    adjacent_positions = [
        tuple_add(current_position, (0,1)),
        tuple_add(current_position, (0,-1)),
        tuple_add(current_position, (1,0)),
        tuple_add(current_position, (-1,0))
    ]
    return list(filter(lambda x: x in map and map[x] == ".", adjacent_positions))

def Puzzle2():
    global target_position

    open_positions = [[target_position]]
    counter = -1
    while len(open_positions) > 0:
        positions = open_positions.pop(0)    
        new_positions = []
        for position in positions:
            map[position] = 'O'
            new_positions.extend(get_positions(position))
        if len(new_positions) > 0:
            open_positions.append(new_positions)
        counter += 1
        
    return counter

if __name__ == "__main__":
    file = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(file.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)
    print("Puzzle 1: " + str(Puzzle1(intcode)))
    print("Puzzle 2: " + str(Puzzle2()))