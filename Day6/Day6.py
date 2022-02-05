spaceObjects = {}


def traverse_space_objects(key, depth):
    if key not in spaceObjects:
        return depth

    orbits = depth
    children = spaceObjects[key]
    for child in children:
        orbits += traverse_space_objects(child, depth + 1)

    return orbits


def Puzzle1():
    child_of_com = spaceObjects["COM"][0]
    return traverse_space_objects(child_of_com, 1)


def Puzzle2():
    return 0


if __name__ == "__main__":
    file = open("input.txt", "r")
    input = file.readlines()

    for line in input:
        parent = line[0:3]
        child = line[4:-1]
        if parent in spaceObjects:
            spaceObjects[parent].append(child)
        else:
            spaceObjects[parent] = [child]
    print("Puzzle 1: " + str(Puzzle1()))
    print("Puzzle 2: " + str(Puzzle2()))
