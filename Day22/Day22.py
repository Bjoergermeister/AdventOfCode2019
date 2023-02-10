def deal_with_increment(stack, increment):
    new_stack = [0] * len(stack)
    for i in range(0, len(stack)):
        new_stack[(i * increment) % len(stack)] = stack[i]
    return new_stack

def cut(stack, amout):
    if amout < 0:
        amout = len(stack) + amout
    
    new_stack = stack[amout:]
    new_stack.extend(stack[0:amout])
    return new_stack 

def Puzzle1(lines):
    stack = list(range(0, 10007))
    for line in lines:
        if line.startswith("deal into new stack"):
            stack.reverse()
        elif line.startswith("cut"):
            divider = line.rindex(" ")
            amout = int(line[divider:])
            stack = cut(stack, amout)
        elif line.startswith("deal with increment"):
            divider = line.rindex(" ")
            increment = int(line[divider:])
            stack = deal_with_increment(stack, increment)
    for i in range(0, len(stack)):
        if stack[i] == 2019:
            return i

if __name__ == "__main__":
    file = open("input.txt")
    lines = file.readlines()
    
    print("Puzzle 1: " + str(Puzzle1(lines)))