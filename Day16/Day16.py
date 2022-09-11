def build_patterns(pattern_count):
    base_pattern = [0, 1, 0, -1]
    patterns = []

    for i in range(1, pattern_count + 1):
        next_pattern = []
        for j in range(len(base_pattern)):
            next_pattern.extend([base_pattern[j]] * i)
        
        patterns.append(next_pattern)
    return patterns

def Puzzle1(input):
    patterns = build_patterns(len(input))

    current_input = input
    for phase in range(0, 100):
        new_input = [0] * len(input)
        for i in range(0, len(input)):
            new_input[i] = abs(sum([value * patterns[i][(index + 1) % len(patterns[i])] for index, value in enumerate(current_input)])) % 10

        current_input = new_input
    
    return "".join(map(lambda number: str(number), current_input[0:8]))


if __name__ == '__main__':
    input = open("input.txt", "r")
    list = [int(number) for number in input.readline()]
    print(f"Puzzle 1: {Puzzle1(list)}")