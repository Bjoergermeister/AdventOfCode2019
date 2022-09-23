moon_positions = []
moon_velocities = []
moon_count = 4

def least_common_multiple(x, y):
    a, b = x, y
    while a:
        a, b = b % a, a
    return x // b * y

def calculate_total_energy() -> int:
    energy = 0
    for index in range(0, moon_count):
        potential_energy = sum(map(abs, moon_positions[index].values()))
        kinetic_energy = sum(map(abs, moon_velocities[index].values()))
        energy += potential_energy * kinetic_energy

    return energy

def puzzle1() -> int:
    total_energy = 0
    step = 0

    states = { 'x': {}, 'y': {}, 'z': {}}
    cycle_times = { 'x': 0, 'y': 0, 'z': 0}

    while any(map(lambda x: cycle_times[x] == 0, cycle_times)): # continue as long as at least one cycle_time is equal to 0
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

        # Keep track of states
        axes = {
            'x': f"{moon_positions[0]['x']}:{moon_positions[1]['x']}:{moon_positions[2]['x']}:{moon_positions[3]['x']}/{moon_velocities[0]['x']}:{moon_velocities[1]['x']}:{moon_velocities[2]['x']}:{moon_velocities[3]['x']}",
            'y': f"{moon_positions[0]['y']}:{moon_positions[1]['y']}:{moon_positions[2]['y']}:{moon_positions[3]['y']}/{moon_velocities[0]['y']}:{moon_velocities[1]['y']}:{moon_velocities[2]['y']}:{moon_velocities[3]['y']}",
            'z': f"{moon_positions[0]['z']}:{moon_positions[1]['z']}:{moon_positions[2]['z']}:{moon_positions[3]['z']}/{moon_velocities[0]['z']}:{moon_velocities[1]['z']}:{moon_velocities[2]['z']}:{moon_velocities[3]['z']}"
        }

        for axis in ['x', 'y', 'z']:
            if cycle_times[axis] != 0:
                continue
            state = axes[axis]
            if state in states[axis]:
                cycle_times[axis] = step - states[axis][state][0]
            else:
                states[axis][state] = [step]

        step += 1    

        if step == 1000:
            total_energy = calculate_total_energy()

    cycle_time = least_common_multiple(cycle_times['x'], least_common_multiple(cycle_times['y'], cycle_times['z']))
    return (total_energy, cycle_time) 

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
    
    (total_energy, cycle_time) = puzzle1()
    print(f"Puzzle 1: {total_energy}")
    print(f"Puzzle 2: {cycle_time}")