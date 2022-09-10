from itertools import permutations

import copy

  
def run(loop, intcode, phase, input, pc = None):

    output = 0
    index = 0 if loop == False else pc
    is_first_input = True if loop == False else pc == 0
    while(intcode[index] != 99):
        instruction = str(intcode[index]).zfill(2)
        
        mode = instruction[-2:]
        is_immediate_mode1 = len(instruction) > 2 and instruction[len(instruction) - 3] == '1'
        is_immediate_mode2 = len(instruction) > 3 and instruction[len(instruction) - 4] == '1'
        is_immediate_mode3 = len(instruction) > 4 and instruction[len(instruction) - 5] == '1'


        if (mode == "01"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = operand1 + operand2
            index += 4
        if (mode == "02"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = operand1 * operand2
            index += 4
        if (mode == "03"):
            position = index + 1 if is_immediate_mode3 else intcode[index + 1]
            if is_first_input:
                intcode[position] = phase
                is_first_input = False
            else:
                intcode[position] = input
            index += 2
        if (mode == "04"):
            output = intcode[index + 1] if is_immediate_mode3 else intcode[intcode[index + 1]] 
            index += 2
            if loop: # If feedback loop mode is on, return here so the next amplifier can continue running. Return the output and the current programm counter
                return output, index, False
        if (mode == "05"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            if operand1 != 0:
                index = operand2
            else:
                index += 3
        if (mode == "06"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            if operand1 == 0:
                index = operand2
            else:
                index += 3
        if (mode == "07"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = 1 if operand1 < operand2 else 0
            index += 4
        if (mode == "08"):
            operand1 = intcode[index + 1] if is_immediate_mode1 else intcode[intcode[index + 1]]
            operand2 = intcode[index + 2] if is_immediate_mode2 else intcode[intcode[index + 2]]
            position = index + 3 if is_immediate_mode3 else intcode[index + 3]
            intcode[position] = 1 if operand1 == operand2 else 0
            index += 4

    if loop:
        return output, index, True
    else:
        return output

def Puzzle1(intcode):
    phases = list(permutations(range(0, 5)))
    input = 0
    highest_output = -1
    for phase in phases:    
        intcodeCopy = copy.deepcopy(intcode)
        output = run(False, intcodeCopy, phase[0], input)
        output = run(False, intcodeCopy, phase[1], output)
        output = run(False, intcodeCopy, phase[2], output)
        output = run(False, intcodeCopy, phase[3], output)
        output = run(False, intcodeCopy, phase[4], output)
        if highest_output == -1 or output > highest_output:
            highest_output = output
    return highest_output

def Puzzle2(intcode):
    phases = list(permutations(range(5, 10)))
    output = 0
    highest_output = -1
    for phase in phases:
        state = [
            { 'intcode': copy.deepcopy(intcode), 'phase_setting': phase[0], 'input': 0, 'pc': 0 },
            { 'intcode': copy.deepcopy(intcode), 'phase_setting': phase[1], 'input': 0, 'pc': 0 },
            { 'intcode': copy.deepcopy(intcode), 'phase_setting': phase[2], 'input': 0, 'pc': 0 },
            { 'intcode': copy.deepcopy(intcode), 'phase_setting': phase[3], 'input': 0, 'pc': 0 },
            { 'intcode': copy.deepcopy(intcode), 'phase_setting': phase[4], 'input': 0, 'pc': 0 }
        ]

        while True:
            is_finished = False
            for i in range(0, 5):
                output, pc, is_finished = run(True, state[i]['intcode'], state[i]['phase_setting'], state[i]['input'], state[i]['pc'])
                if is_finished == False:
                    state[i]['pc'] = pc
                    index = i + 1 if i < 4 else 0
                    state[index]['input'] = output

            if is_finished:
                break

        if highest_output == -1 or state[0]['input'] > highest_output:
            highest_output = state[0]['input']

    return highest_output

if __name__ == "__main__":
    input = open("input.txt", "r")
    numbers = [int(x) for x in input.readline().split(",")]
    print("Puzzle 1: " + str(Puzzle1(numbers)))
    print("Puzzle 2: " + str(Puzzle2(numbers)))
