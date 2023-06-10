import copy


class State:
    def __init__(self, intcode, network_address):
        self.intcode = copy.deepcopy(intcode)
        self.network_address = network_address
        self.input = []
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
        else:
            input = state.input.pop(0) if len(state.input) > 0 else -1
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


def network_is_idle(states):
    return all(len(state.input) == 0 for state in states)


def Puzzle1(intcode):
    states = [State(intcode, i) for i in range(0, 50)]

    first_answer = 0

    nat_packet = None
    latest_nat_delivery = None
    while True:
        for state in states:
            packet = run(state)
            if packet is None:
                continue

            destination_index = packet[0]
            message = packet[1:3]
            if destination_index != 255:
                states[destination_index].input.extend(message)
                state.outputs.clear()
                continue

            first_answer = max(first_answer, message[1])

            nat_packet = message.copy()
            if network_is_idle(states):
                states[0].input.extend(nat_packet)
                if nat_packet is not None and latest_nat_delivery is not None and nat_packet[1] == latest_nat_delivery[1]:
                    return first_answer, nat_packet[1]
                latest_nat_delivery = list(nat_packet)
            state.outputs.clear()


if __name__ == "__main__":
    input = open("input.txt", "r")
    intcode = {}
    for index, number in enumerate(input.readline().split(",")):
        intcode[index] = int(number)
    intcodeCopy = copy.deepcopy(intcode)

    answer1, answer2 = Puzzle1(intcode)
    print("Puzzle 1: " + str(answer1))
    print("Puzzle 2: " + str(answer2))
