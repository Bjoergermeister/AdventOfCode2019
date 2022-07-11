import math

asteroids = []
         
def puzzle1():
    max_length = -1
    for asteroid in asteroids:
        angles = dict()
        for other_asteroid in asteroids:
            if asteroid == other_asteroid:
                continue
            angle = math.atan2(asteroid[0] - other_asteroid[0], asteroid[1] - other_asteroid[1]) * (180 / math.pi)
            if angle in angles:
                angles[angle].append(other_asteroid)
            else:
                angles[angle] = [other_asteroid]
        
        if len(angles) > max_length:
            max_length = len(angles)
    return max_length

if __name__ == "__main__":
    file = open("input.txt", "r")
    lines = file.readlines()
    for x in range(0, len(lines)):
        for y in range(0, len(lines[-1])):
            if lines[y][x] == '#':
                asteroids.append((x, y))
    print(f"Puzzle 1: {puzzle1()}")
    #count()