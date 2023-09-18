import copy
import os
import re

relative_base = 0
output = 0
index = 0

OPPOSITE_DIRECTIONS = {
    None: None,
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east",
}

DIRECTIONS_VECTORS = {
    "north": (0, 1),
    "east": (1, 0),
    "south": (0, -1),
    "west": (-1, 0),
}

COMMANDS = {
    None: None,
    "north": [ord(character) for character in f"north{chr(10)}"],
    "east": [ord(character) for character in f"east{chr(10)}"],
    "south": [ord(character) for character in f"south{chr(10)}"],
    "west": [ord(character) for character in f"west{chr(10)}"],
    "inv": [ord(character) for character in f"inv{chr(10)}"]
}

def get_index(intcode, index, mode):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base


def run(intcode, command):
    global relative_base, output, index

    # Puzzle variables
    current_room_name = ""
    current_section_list = None
    next_directions = []
    items = []
    line = ""
    previous_operand = None

    while(intcode[index] != 99):
        instruction = str(intcode[index]).zfill(2)

        mode = instruction[-2:]
        operand1_mode = instruction[len(
            instruction) - 3] if len(instruction) > 2 else '0'
        operand2_mode = instruction[len(
            instruction) - 4] if len(instruction) > 3 else '0'
        operand3_mode = instruction[len(
            instruction) - 5] if len(instruction) > 4 else '0'

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
            intcode[index1] = command.pop(0)
            index += 2
        if (mode == "04"):
            #print(chr(operand1), end="")
            index += 2

            if operand1 == 10:
                # Droid is asking for a command
                if line == "Command?":
                    return current_room_name, next_directions, set(items)

                # This is the name of the current room
                if line.startswith("=="):
                    current_room_name = line[3:-3]

                # Droid prints information about possible directions or items
                if previous_operand == ord(":"):
                    if line.startswith("Doors"):
                        current_section_list = next_directions
                    else:
                        current_section_list = items

                # This marks the beginning of the direction or items section
                if line.startswith("-"):
                    current_section_list.append(line[2:])

                if line.startswith("\""):
                    return int(re.findall(r'\d+', line)[0])

                line = ""
            else:
                line += chr(operand1)
            previous_operand = operand1
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


def build_item_command(action, item):
    return [ord(character) for character in f"{action} {item}{chr(10)}"]

def print_command(command):
    print("".join([chr(character) for character in command]))

def collect_items(intcode):
    room_name = ""
    old_room_name = ""
    states = {}
    dont_take = {"photons", "molten lava", "infinite loop", "escape pod", "giant electromagnet"}
    directions = None
    last_direction = None
    command = None
    carried_items = []
    while True:

        if room_name == "Hull Breach" and next_direction == None:
            return carried_items

        room_name, next_directions, items = run(intcode, command)

        old_room_name = room_name if room_name != "" else old_room_name
        room_name = old_room_name

        # Update state
        if room_name != "" and room_name not in states:
            states[room_name] = { 'directions': next_directions, 'backtrack': OPPOSITE_DIRECTIONS[last_direction] }       
        directions = states[room_name]["directions"] if room_name != "" else directions

        takeable_items = items.difference(dont_take)
        if len(takeable_items) > 0:
            command = build_item_command("take", list(items)[0])
            carried_items.append(list(items)[0])
            continue
        
        next_direction = None
        if len(directions) == 0:
            next_direction = states[room_name]["backtrack"]
        elif len(directions) > 1 and directions[0] == states[room_name]["backtrack"]:
            next_direction = directions[1]
        else:
            next_direction = directions[0]

        if next_direction is not None:
            command = COMMANDS[next_direction].copy()
            last_direction = next_direction

        # Update position and track possible directions
        if next_direction in states[room_name]["directions"]:
            states[room_name]["directions"].remove(next_direction)

def walk_to_security_door(intcode, items):
    inventory = [1 for item in items]
    inventory_commands = ["drop", "take"]
    direction_list = ["west", "south", "west"]
    for direction in direction_list:
        command = COMMANDS[direction].copy()
        run(intcode, command)

    bit_pattern = 0
    max_iterations = pow(2, len(items))
    while bit_pattern < max_iterations:
        result = [int((bit_pattern & 1 << item_index) / (1 << item_index)) for item_index in range(0, len(items))] 
        for i in range(0, 8):
            if result[i] != inventory[i]:
                inventory[i] = result[i]
                command = build_item_command(inventory_commands[result[i]], items[i])
                run(intcode, command)
        value = run(intcode, COMMANDS["south"].copy())
        if type(value) == int:
            return value

        bit_pattern += 1

def Puzzle1(intcode):
    items = collect_items(intcode)
    return walk_to_security_door(intcode, items)

if __name__ == "__main__":
    input_file_name = "input.txt" if "2019" in os.getcwd() else "2019/Day25/input.txt"
    input_file = open(input_file_name, "r")
    intcode = {}
    for input_index, number in enumerate(input_file.readline().split(",")):
        intcode[input_index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)

    print("Puzzle 1: " + str(Puzzle1(intcode)))
