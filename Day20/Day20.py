from os import system
from time import sleep


MAP_WIDTH = 109
MAP_HEIGHT = 115
DIRECTIONS = [-1, -MAP_WIDTH, 1, MAP_WIDTH]
PORTAL_POSITIONS = {}
PORTAL_DIRECTIONS = {}
CROSSINGS = set()
ENDPOINTS = set()
STATES = {}
MAP = []
START_POSITION = None
END_POSITION = None

class State():

    def __init__(self, moving_direction, distance):
        self.directions = [direction for direction in DIRECTIONS if moving_direction is None or direction != moving_direction * -1]
        self.direction_index = 0
        self.previous_direction = None if moving_direction is None else moving_direction * -1
        self.distance = distance
        
    def direction(self):
        if self.direction_index < len(self.directions):
            return self.directions[self.direction_index]
        return self.previous_direction

    def is_backtracking(self):
        return self.direction_index >= len(self.directions)

def hash_portal(position, vector):
    part_one = ord(MAP[position + vector]) - 64
    part_two = ord(MAP[position + vector + vector]) - 64
    hash = pow(part_one, 2) + pow(part_two, 2)
    return hash

def parse_portal(portals, position, direction):
    global START_POSITION, END_POSITION
    portal_hash = hash_portal(position, direction)
    if portal_hash == 2:
        START_POSITION = position
    elif portal_hash == 1352:
        END_POSITION = position
    elif portal_hash in portals:
        portals[portal_hash].append(position)
    else:
        portals[portal_hash] = [position]
            
    PORTAL_DIRECTIONS[position] = direction

def find_portals():
    global START_POSITION, END_POSITION, PORTAL_POSITIONS, PORTAL_DIRECTIONS
    portals = {}
    for i in range(len(MAP)):
        if MAP[i] != '.':
            continue

        way_count = 0
        for direction in DIRECTIONS:
            position = i + direction
            if ord(MAP[position]) >= 65: # It's a portal
                parse_portal(portals, i, direction)
            elif MAP[position] == '.':
                way_count += 1

        if way_count <= 1 and i not in portals and i != START_POSITION and i != END_POSITION:
            ENDPOINTS.add(i)
        if way_count >= 3:
            CROSSINGS.add(i)

    for portal in portals.values():
        PORTAL_POSITIONS[portal[0]] = portal[1]
        PORTAL_POSITIONS[portal[1]] = portal[0]

    for portal_position in PORTAL_POSITIONS:
        if portal_position in ENDPOINTS:
            ENDPOINTS.remove(portal_position)

def is_portal(position):
    character = ord(MAP[position])
    return character >= 65 and character <= 91

def update_states(position, direction, distance):
    global STATES

    if position not in STATES:        
        STATES[position] = State(direction, distance)
        return STATES[position]
    state = STATES[position]
    state.distance = min(distance, state.distance)
    return state

def find_crossing(current_position):
    while True:
        state = STATES[current_position]

        if current_position == END_POSITION:
            return 1, state.distance
        while MAP[current_position + state.direction()] == '#': # Dont walk into a wall
            state.direction_index += 1
        if MAP[current_position + state.direction()] != ".": # Reached a portal
            state.direction_index += 1
            if current_position == END_POSITION:
                continue
            
            current_position = PORTAL_POSITIONS[current_position] # Get position of other part of the portal
            portal_direction = PORTAL_DIRECTIONS[current_position] * -1
            state = update_states(current_position, portal_direction, state.distance + 1)
        else: # Normal position
            current_position = current_position + state.direction()
            next_state = update_states(current_position, state.direction(), state.distance + 1)
            state.direction_index += 1
            state = next_state

        if current_position in ENDPOINTS:
            return None, None

        if current_position in CROSSINGS:
            return 0, current_position

def Puzzle1():
    STATES[START_POSITION] = State(None, 0)
    CURRENT_POSITIONS = [START_POSITION]
    NEXT_POSITIONS = []

    # Move
    while True:
        for position in CURRENT_POSITIONS: 
            state = STATES[position]
            while state.is_backtracking() == False:
                '''
                Return Codes:
                 0 - Found next crossing
                 1 - Found end
                 2 - Reachted dead end
                '''
                code, output = find_crossing(position)
                if code == 0:
                    NEXT_POSITIONS.append(output)
                elif code == 1:
                    return output

                if position == START_POSITION:
                    break

        CURRENT_POSITIONS.clear()
        CURRENT_POSITIONS.extend(NEXT_POSITIONS)
        NEXT_POSITIONS.clear()

        if len(CURRENT_POSITIONS) == 0:
            return 0

if __name__ == "__main__":
    input = open("input.txt")
    lines = input.readlines()
    
    # Transform lines into array
    for line in lines:
        for position in line[:-1]:
            MAP.append(position)
    
    find_portals()
    print("Puzzle 1: ", str(Puzzle1()))