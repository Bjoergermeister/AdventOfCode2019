import copy


class State:
    def __init__(self, intcode, network_address):
        self.intcode = copy.deepcopy(intcode)
        self.network_address = network_address
        self.packet_queue = []
        self.outputs = []
        self.index = 0
        self.relative_base = 0
        self.is_first_input = True

    def __str__(self):
        return f"{self.intcode}, {self.network_address}"


def get_index(intcode, index, mode, relative_base):
    if mode == '0':
        return intcode[index] if index in intcode else 0
    if mode == '1':
        return index
    if mode == '2':
        return intcode[index] + relative_base


def run(state):
    # Intcode vars
    intcode = state.intcode
    index = state.index

    instruction = str(intcode[index]).zfill(2)

    mode = instruction[-2:]
    operand1_mode = instruction[len(
        instruction) - 3] if len(instruction) > 2 else '0'
    operand2_mode = instruction[len(
        instruction) - 4] if len(instruction) > 3 else '0'
    operand3_mode = instruction[len(
        instruction) - 5] if len(instruction) > 4 else '0'

    index1 = get_index(intcode, index + 1, operand1_mode, state.relative_base)
    index2 = get_index(intcode, index + 2, operand2_mode, state.relative_base)
    index3 = get_index(intcode, index + 3, operand3_mode, state.relative_base)

    operand1 = intcode[index1] if index1 in intcode else 0
    operand2 = intcode[index2] if index2 in intcode else 0

    if (mode == "01"):
        intcode[index3] = operand1 + operand2
        index += 4
    if (mode == "02"):
        intcode[index3] = operand1 * operand2
        index += 4
    if (mode == "03"):
        input = None
        if state.is_first_input:
            input = state.network_address
            state.is_first_input = False
        elif len(state.packet_queue) == 0:
            input = -1
        else:
            input = state.packet_queue[0].pop(0)
            if len(state.packet_queue[0]) == 0:
                del state.packet_queue[0]
        intcode[index1] = input
        index += 2
    if (mode == "04"):
        state.outputs.append(operand1)
        index += 2
    if (mode == "05"):
        index = operand2 if operand1 != 0 else index + 3
    if (mode == "06"):
        index = operand2 if operand1 == 0 else index + 3
    if (mode == "07"):
        intcode[index3] = 1 if operand1 < operand2 else 0
        index += 4
    if (mode == "08"):
        intcode[index3] = 1 if operand1 == operand2 else 0
        index += 4
    if (mode == "09"):
        state.relative_base += operand1
        index += 2

    state.intcode = intcode
    state.index = index
    return state.outputs if len(state.outputs) == 3 else None


def Puzzle1(intcode):
    states = [State(intcode, i) for i in range(0, 50)]
    while True:
        for state in states:
            packet = run(state)
            if packet is None:
                continue

            destination_index = packet[0]
            if destination_index == 255:
                return packet[2]

            states[destination_index].packet_queue.append(packet[1:3])
            state.outputs.clear()


if __name__ == "__main__":
    input = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(input.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)
    print("Puzzle 1: " + str(Puzzle1(intcode)))
