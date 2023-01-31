def Puzzle1(input):
    current_input = input
    for phase in range(0, 100):
        for i in range(0, len(input)):
            pattern_length = i * 4 + 4

            total = 0
            pattern_offset = 0
            while pattern_offset < len(input):
                pattern_section_size = pattern_length // 4
                positive_begin = pattern_offset + (pattern_section_size - 1)
                positive_end = pattern_offset + (pattern_section_size * 2 - 1)
                negative_begin = pattern_offset + (pattern_section_size * 3 - 1)
                negative_end = pattern_offset + (pattern_section_size * 4 - 1)
                
                sum_positive = sum(current_input[positive_begin:positive_end])
                sum_negative = sum(current_input[negative_begin:negative_end])

                total += sum_positive
                total -= sum_negative

                pattern_offset += pattern_length
            current_input[i] = abs(total) % 10
    
    return "".join(map(lambda number: str(number), current_input[0:8]))

def Puzzle2(long_list):
    offset = 0
    for i in range(0, 7):
        offset = (offset * 10) + long_list[i]
    
    for phase in range(0, 100):
        for i in reversed(range(offset, len(long_list) - 1)):
            long_list[i] = (long_list[i] + long_list[i + 1]) % 10                
    return ''.join(map(lambda x: str(x), long_list[offset:offset+8])) # Convert list of number to string
        
if __name__ == '__main__':
    input = open("input.txt", "r")
    list = [int(number) for number in input.readline()]
    long_list = list.copy() * 10000

    print(f"Puzzle 1: {Puzzle1(list)}")
    print(f"Puzzle 2: {Puzzle2(long_list)}")