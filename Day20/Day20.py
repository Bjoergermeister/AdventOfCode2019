MAP_WIDTH = 0
MAP_HEIGHT = 0
DIRECTIONS = []
PORTAL_POSITIONS = {}
PORTAL_DIRECTIONS = {}
CROSSINGS = set()
ENDPOINTS = set()
STATES = {}
MAP = []
START_POSITION = None
END_POSITION = None
AA_HASH = 2
ZZ_HASH = 1352

LEVEL = 0
MODE = 1 # 1 = Puzzle 1, 2 = Puzzle 2

# Lambdas which check if a portal is on the outside of the maze
is_top = lambda position: (MAP_WIDTH * 2 + 2) <= position <= (MAP_WIDTH * 3 - 2)
is_bottom = lambda position: (MAP_WIDTH * (MAP_HEIGHT - 3) + 2) <= position <= (MAP_WIDTH * (MAP_HEIGHT - 2) - 2)
is_left = lambda position: position % MAP_WIDTH == 2
is_right = lambda position: position % MAP_WIDTH == MAP_WIDTH - 3

class Position():
    def __init__(self, level, coordinates):
        self.level = level
        self.coordinates = coordinates

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
    
    def get_directions(self):
        return self.directions

def hash_portal(position, vector):
    part_one = ord(MAP[position + vector]) - 64
    part_two = ord(MAP[position + vector + vector]) - 64
    hash = pow(part_one, 2) + pow(part_two, 2)
    return hash

def parse_portal(portals, position, direction):
    global START_POSITION, END_POSITION
    portal_hash = hash_portal(position, direction)
    if portal_hash == AA_HASH: # 2 is the hash of the AA portal, so the starting position
        START_POSITION = position
    elif portal_hash == ZZ_HASH: # 1352 is the hash of the ZZ portal, so the destination
        END_POSITION = position
    elif portal_hash in portals:
        portals[portal_hash].append(position)
    else:
        portals[portal_hash] = [position]
            
    PORTAL_DIRECTIONS[position] = direction

def find_portals():
    global START_POSITION, END_POSITION, PORTAL_POSITIONS, PORTAL_DIRECTIONS
    portals = {}
    find_endpoints_and_crossings(portals, True)

    for portal in portals.values():
        PORTAL_POSITIONS[portal[0]] = portal[1]
        PORTAL_POSITIONS[portal[1]] = portal[0]

    for portal_position in PORTAL_POSITIONS:
        if portal_position in ENDPOINTS:
            ENDPOINTS.remove(portal_position)

def is_portal(position, direction, level):
    if (position == END_POSITION and level != 0) or position == START_POSITION:
        return False

    next_position = position + direction
    character = ord(MAP[next_position])
    is_portal = character >= 65 and character <= 91

    if is_portal == False:
        return False

    # In mode 1, every portal is an actual portal
    if MODE == 1:
        return is_portal
    
    # In mode 2, outside portals are not considered portals if the level is 0
    return is_outside_portal(position) == False or level > 0

def is_outside_portal(position):
    return is_top(position) or is_bottom(position) or is_left(position) or is_right(position)

def get_position_hash(coordinates, level):
    return f"{level}_{coordinates}"

def update_states(coordinates, level, direction, distance):
    global STATES

    position_hash = get_position_hash(coordinates, level)
    if position_hash not in STATES:        
        STATES[position_hash] = State(direction, distance)
        return STATES[position_hash]
    state = STATES[position_hash]
    state.distance = min(distance, state.distance)
    return state

def is_wall(position):
    return MAP[position] == '#'

def find_endpoints_and_crossings(portals, parse_portals):
    for i in range(len(MAP)):
        if MAP[i] != '.':
            continue

        way_count = 0
        for direction in DIRECTIONS:
            position = i + direction
            if ord(MAP[position]) >= 65 and parse_portals: # It's a portal
                parse_portal(portals, i, direction)
            elif MAP[position] == '.':
                way_count += 1

        if way_count == 1 and i not in portals and i != START_POSITION and i != END_POSITION:
            ENDPOINTS.add(i)
        if way_count >= 3:
            CROSSINGS.add(i)

def eliminate_dead_ends():
    while len(ENDPOINTS) > 0:
        for endpoint in ENDPOINTS:
            position = endpoint
            # Walk the grid until a crossing is found
            while True:      
                direction_index = 0
                while MAP[position + DIRECTIONS[direction_index]] != '.':
                    direction_index += 1

                next_position = position + DIRECTIONS[direction_index]

                if next_position in CROSSINGS:
                    MAP[position] = '#'
                    break
                else:
                    MAP[position] = ' '
                    position = next_position

        # Reset crossing and endpoint lists and find the new ones
        ENDPOINTS.clear()
        CROSSINGS.clear()

        find_endpoints_and_crossings(PORTAL_POSITIONS, False)

def is_endpoint(coordinates, level):
    if coordinates in ENDPOINTS:
        return True

    # Other positions than the list of endpoints are only consideres as endpoints in MODE 2    
    if MODE == 1:
        return False

    if level > 0 and (coordinates == START_POSITION or coordinates == END_POSITION):
        return True
    
    return level == 0 and is_outside_portal(coordinates) and coordinates not in [START_POSITION, END_POSITION]

def find_crossing(current_position):
    global LEVEL, MODE

    coordinates = current_position.coordinates
    level = current_position.level

    while True:
        state = STATES[get_position_hash(coordinates, level)]
        if coordinates == END_POSITION and level == 0:
            return 1, state.distance
        
        # Dont walk into a wall
        while is_wall(coordinates + state.direction()):
            state.direction_index += 1
        
        if is_portal(coordinates, state.direction(), level):
            if MODE == 2:
                level += -1 if is_outside_portal(coordinates) else 1

            state.direction_index += 1
            coordinates = PORTAL_POSITIONS[coordinates] # Get position of other part of the portal
            portal_direction = PORTAL_DIRECTIONS[coordinates] * -1

            state = update_states(coordinates, level, portal_direction, state.distance + 1)        
        elif is_endpoint(coordinates, level):
            return 2, None
        else: # Normal position
            coordinates = coordinates + state.direction()
            next_state = update_states(coordinates, level, state.direction(), state.distance + 1)
            state.direction_index += 1
            state = next_state

        if coordinates in CROSSINGS:
            next_positions = []
            for direction in state.get_directions():
                next_coordinate = coordinates + direction
                if MAP[next_coordinate] != '.':
                    continue
                
                next_positions.append(Position(level, next_coordinate))
                update_states(next_coordinate, level, direction, state.distance + 1)
            return 0, next_positions

def run():
    STATES[get_position_hash(START_POSITION, 0)] = State(None, 0)
    CURRENT_POSITIONS = [Position(0, START_POSITION)]
    NEXT_POSITIONS = []

    # Move
    while True:
        for position in CURRENT_POSITIONS: 
            state = STATES[get_position_hash(position.coordinates, position.level)]
            while state.is_backtracking() == False:
                '''
                Return Codes:
                 0 - Found next crossing
                 1 - Found end
                 2 - Reached dead end
                '''
                code, output = find_crossing(position)
                if code == 0:# and output not in known_positions:
                    NEXT_POSITIONS.extend(output)
                elif code == 1:
                    return output
                else:
                    break

                if position.coordinates == START_POSITION:
                    break

        CURRENT_POSITIONS.clear()
        CURRENT_POSITIONS.extend(NEXT_POSITIONS)
        NEXT_POSITIONS.clear()

        if len(CURRENT_POSITIONS) == 0:
            return 0

if __name__ == "__main__":
    text = open("input.txt")
    lines = text.readlines()
    
    # Transform lines into array
    MAP_HEIGHT = len(lines)
    MAP_WIDTH = len(lines[0][:-1])
    DIRECTIONS = [-1, -MAP_WIDTH, 1, MAP_WIDTH]
    for line in lines:
        for position in line[:-1]:
            MAP.append(position)
    
    find_portals()

    print("Puzzle 1: ", str(run()))
   
    eliminate_dead_ends()
    # Reset data structures
    MODE = 2
    STATES = {}
    VISITED_CROSSINGS = {}
    
    print("Puzzle 2: ", str(run()))