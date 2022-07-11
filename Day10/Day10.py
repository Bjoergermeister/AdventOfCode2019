import math

asteroids = []
monitoring_station_angles = None
         
def puzzle1():
    global monitoring_station_angles
    max_length = -1
    for asteroid in asteroids:
        angles = dict()
        for other_asteroid in asteroids:
            if asteroid == other_asteroid:
                continue

            x1, y1 = asteroid
            x2, y2 = other_asteroid
            distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
            angle = math.atan2(x1 - x2, y1 - y2) * (180 / math.pi)
            if angle not in angles or distance < angles[angle][1]:
                angles[angle] = (other_asteroid, distance)
        
        if len(angles) > max_length:
            max_length = len(angles)
            monitoring_station_angles = angles
    return max_length

def puzzle2():
    sorted_angles = list(reversed(sorted(monitoring_station_angles.keys())))
    zero_angle_index = sorted_angles.index(0.0)

    count = 1
    index = zero_angle_index
    while True:
        if count == 200:
            asteroid = monitoring_station_angles[sorted_angles[index]][0]
            return asteroid[0] * 100 + asteroid[1]
        index += 1
        count += 1
        if index == len(sorted_angles):
            index = 0
        if index == zero_angle_index:
            break

if __name__ == "__main__":
    file = open("input.txt", "r")
    lines = file.readlines()
    for y in range(0, len(lines)):
        for x in range(0, len(lines[-1])):
            if lines[y][x] == '#':
                asteroids.append((x, y))
    print(f"Puzzle 1: {puzzle1()}")
    print(f"Puzzle 2: {puzzle2()}")