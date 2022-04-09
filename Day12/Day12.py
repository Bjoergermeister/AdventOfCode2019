moon_positions = []
moon_velocities = []
moon_count = 4

def calculate_total_energy() -> int:
    energy = 0
    for index in range(0, moon_count):
        potential_energy = sum(map(abs, moon_positions[index].values()))
        kinetic_energy = sum(map(abs, moon_velocities[index].values()))
        energy += potential_energy * kinetic_energy

    return energy

def puzzle1() -> int:
    for step in range(0, 1000):
        # Apply gravity to all pairs of moons
        for i in range(0, moon_count - 1):
            for j in range(i + 1, moon_count):
                for axis in ['x', 'y', 'z']:
                    first_coordinate = moon_positions[i][axis]
                    first_velocity = moon_velocities[i][axis]

                    second_coordinate = moon_positions[j][axis]
                    second_velocity = moon_velocities[j][axis]


                    if first_coordinate == second_coordinate:
                        continue

                    moon_velocities[i][axis] = first_velocity + 1 if first_coordinate < second_coordinate else first_velocity - 1
                    moon_velocities[j][axis] = second_velocity + 1 if second_coordinate < first_coordinate else second_velocity - 1

        # Update positions
        for i in range(0, moon_count):
            for axis in ['x', 'y', 'z']:
                moon_positions[i][axis] += moon_velocities[i][axis]
    
    return calculate_total_energy()

if __name__ == "__main__":
    file = open("input.txt", "r")
    lines = file.readlines()
    for index, line in enumerate(lines):
        moon_position = {}
        for position in line[1:-2].split(", "):
            [axis, coordinate] = position.split("=")
            moon_position[axis] = int(coordinate)
        moon_positions.append(moon_position)
        moon_velocities.append({ 'x': 0, 'y': 0, 'z': 0 })

    print(f"Puzzle 1: {puzzle1()}")