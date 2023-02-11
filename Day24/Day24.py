FIELD_SIZE = 25

def is_alive(field, x, y):
    if x < 0 or x > 4 or y < 0 or y > 4:
        return False
    return field[y * 5 + x] == 1

def calculate_next_state(active_field, passive_field):
    fields_to_check = [(1,0), (-1,0), (0,1), (0,-1)]
    for i in range(0, 25):
        y = i // 5
        x = i % 5
        alive = 0
        for field in fields_to_check:
            xx = x + field[0]
            yy = y + field[1]
            if is_alive(active_field, xx, yy):
                alive += 1
        if active_field[i] == 1 and alive != 1:
            passive_field[i] = 0
        elif active_field[i] == 0 and (alive == 1 or alive == 2):
            passive_field[i] = 1
        else:
            passive_field[i] = active_field[i]

    return passive_field, active_field

def calculate_sum(field):
    sum = 0
    for i in range(0, 25):
        sum += field[i] * pow(2,i)
    return sum

def Puzzle1(lines):
    active_field = [0] * FIELD_SIZE
    passive_field = [0] * FIELD_SIZE
    sums = []

    # Initialize
    for i in range(0, 25):
        line_index = i // 5
        active_field[i] = 0 if lines[line_index][i % 5] == '.' else 1

    while True:
        active_field, passive_field = calculate_next_state(active_field, passive_field)

        sum = calculate_sum(active_field)
        if sum in sums:
            return sum
        sums.append(sum)

if __name__ == "__main__":
    file = open("input.txt")
    lines = file.readlines()

    print("Puzzle 1: " + str(Puzzle1(lines)))