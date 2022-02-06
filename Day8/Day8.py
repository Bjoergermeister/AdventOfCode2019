input = []
image_width = 25
image_height = 6
layers = []
layer_size = image_width * image_height


def Puzzle1(input):
    layer = []
    lowest_zero_count = -1
    zero_count = 0
    layer_with_fewest_zero_digits = 0

    for i in range(len(input)):
        if i % layer_size == 0 and i > 0:
            if zero_count < lowest_zero_count or lowest_zero_count < 0:
                lowest_zero_count = zero_count
                layer_with_fewest_zero_digits = (i // layer_size) - 1

            zero_count = 0
            layers.append(layer)
            layer = []
        next_digit = input[i]

        if next_digit == '0':
            zero_count += 1
        layer.append(next_digit)

    ones = 0
    twos = 0
    for number in layers[layer_with_fewest_zero_digits]:
        if number == '1':
            ones += 1
        if number == '2':
            twos += 1

    return ones * twos


def Puzzle2(input):
    pass


if __name__ == "__main__":
    file = open("input.txt", "r")
    input = file.readlines()[0]
    print("Puzzle 1: " + str(Puzzle1(input)))
    print("Puzzle 2: " + str(Puzzle2(input)))
