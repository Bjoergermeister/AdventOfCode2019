spaceObjects = {}
distances_to_santa = {}
distances_to_me = {}


def traverse_space_objects(key, depth):
    if key not in spaceObjects:
        return -1, -1, depth

    santa_depth = -1
    my_depth = -1
    orbits = depth
    children = spaceObjects[key]
    for child in children:
        if child == "YOU":
            my_depth = depth
        if child == "SAN":
            santa_depth = depth
        my_depth_current, santa_depth_current, new_orbits = traverse_space_objects(
            child, depth + 1)
        orbits += new_orbits
        if my_depth_current != -1:
            my_depth = my_depth_current
            distances_to_me[key] = my_depth - depth
        if santa_depth_current != -1:
            santa_depth = santa_depth_current
            distances_to_santa[key] = santa_depth - depth

    return my_depth, santa_depth, orbits


def Puzzle1():
    child_of_com = spaceObjects["COM"][0]
    m, s, total_orbits = traverse_space_objects(child_of_com, 1)
    return total_orbits


def Puzzle2():
    smallest_distance = -1
    for key in distances_to_me:
        if key in distances_to_santa:
            distance = distances_to_me[key] + distances_to_santa[key]
            if smallest_distance == -1 or smallest_distance > distance:
                smallest_distance = distance
    return smallest_distance


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
