FIELD_SIZE = 25

active_levels = {}
passive_levels = {}
is_part_two = False

def sign(value):
    if value == 0:
        return 0
    return 1 if value > 0 else -1

def check_field_part_two(field, x, y, xx, yy, level):
    if (xx == -1 or xx == 5):
        return passive_levels[level - 1][12 + sign(xx)] # 12 is the middle of the field, so this gives either the left or the right of the middle
    
    if (yy == -1 or yy == 5): 
        return passive_levels[level - 1][12 + (sign(yy) * 5)] # same as above, but this time above and below the middle
    
    if xx == 2 and yy == 2:
        required_fields = None

        x_diff = xx - x
        y_diff = yy - y
        if x_diff == 0:
            target_y = 0 if y_diff == 1 else 4
            required_fields = [(i, target_y) for i in range(0, 5)]
        else:
            target_x = 0 if x_diff == 1 else 4
            required_fields = [(target_x, i) for i in range(0, 5)]

        return sum([active_levels[level + 1][pos_y * 5 + pos_x] for (pos_x, pos_y) in required_fields])
        
    return field[yy * 5 + xx]

def count_neighbours(field, x, y, level):
    neighbours = 0
    fields_to_check = [(x + 1,y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for (xx, yy) in fields_to_check:
        if is_part_two:
            neighbours += check_field_part_two(field, x, y, xx, yy, level)
        else:
            if xx < 0 or xx > 4 or yy < 0 or yy > 4:
                continue
            neighbours += field[yy * 5 + xx]
    return neighbours

def calculate_next_state(active_field, passive_field, level):
    for i in range(0, 25):
        y = i // 5
        x = i % 5

        if is_part_two and x == 2 and y == 2:
            continue

        neighbours = count_neighbours(active_field, x, y, level)
        if active_field[i] == 1 and neighbours != 1:
            passive_field[i] = 0
        elif active_field[i] == 0 and (neighbours == 1 or neighbours == 2):
            passive_field[i] = 1
        else:
            passive_field[i] = active_field[i]

    return passive_field, active_field

def calculate_sum(field):
    sum = 0
    for i in range(0, 25):
        sum += field[i] * pow(2,i)
    return sum

def initialize_field(lines):
    field = [0] * FIELD_SIZE
    for i in range(0, 25):
        line_index = i // 5
        field[i] = 0 if lines[line_index][i % 5] == '.' else 1
    return field

def Puzzle1(lines):
    active_field = initialize_field(lines)
    passive_field = [0] * FIELD_SIZE
    sums = []

    while True:
        active_field, passive_field = calculate_next_state(active_field, passive_field, 0)

        sum = calculate_sum(active_field)
        if sum in sums:
            return sum
        sums.append(sum)

def Puzzle2(lines):
    active_levels[0] = initialize_field(lines)
    passive_levels[0] = [0] * FIELD_SIZE
    highest_level = 1
    lowest_level = -1

    for i in (-1, 1):
        active_levels[i] = [0] * FIELD_SIZE
        passive_levels[i] = [0] * FIELD_SIZE

    for i in range(200):
        # Add new levels
        active_levels[highest_level + 1] = [0] * FIELD_SIZE
        active_levels[lowest_level - 1] = [0] * FIELD_SIZE
        passive_levels[highest_level + 1] = [0] * FIELD_SIZE
        passive_levels[lowest_level - 1] = [0] * FIELD_SIZE

        index = lowest_level
        while index <= highest_level:
            active_levels[index], passive_levels[index] = calculate_next_state(active_levels[index], passive_levels[index], index)
            index += 1

        highest_level += 1
        lowest_level -= 1

    total_sum = 0
    for level in active_levels:
        total_sum += sum(active_levels[level])
    return total_sum

if __name__ == "__main__":
    file = open("input.txt")
    lines = file.readlines()

    print("Puzzle 1: " + str(Puzzle1(lines)))
    is_part_two = True
    print("Puzzle 2: " + str(Puzzle2(lines)))