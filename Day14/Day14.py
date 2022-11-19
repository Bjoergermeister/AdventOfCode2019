from math import ceil

reactions = {}
leftovers = {}
#ore_reactions = ["NVRVD", "JNWZP", "MNCFX", "VJHF"]
ore_reactions = []

def parse_element(element):
    [cost, name] = element.split()
    return (name, int(cost))

def update_element_quantity(needed_elements, new_elements):
    for new_element in new_elements: 
        index_to_update = None       
        for index, element in enumerate(needed_elements):
            if element[0] == new_element[0]:
                index_to_update = index

        if index_to_update is None:
            needed_elements.append(new_element)
        else:
            needed_elements[index_to_update] = (new_element[0], needed_elements[index_to_update][1] + new_element[1])

def get_item_index(needed_elements):
    for i in range(len(needed_elements)):
        if needed_elements[i][0] not in ore_reactions:
            return i

    return None

def puzzle1():
    needed_elements = [('FUEL', 1)]
    total_costs = 0

    while True:
        index = get_item_index(needed_elements)
        if index is None:
            break

        (needed_element, needed_amout) = needed_elements.pop(index)
        if needed_element in leftovers:
            needed_amout -= leftovers[needed_element]
            leftovers[needed_element] = 0

        (reaction_output, reaction_inputs) = reactions[needed_element]
        reaction_quantity = ceil(needed_amout / reaction_output)
        leftovers[needed_element] = reaction_output * reaction_quantity - needed_amout

        if len(reaction_inputs) == 1 and reaction_inputs[0][0] == "ORE":
            continue

        reaction_quantity = ceil(needed_amout / reaction_output)
        update_element_quantity(needed_elements, map(lambda value: (value[0], value[1] * reaction_quantity), reaction_inputs))
    
    for (element, amout) in needed_elements:
            reaction = reactions[element]
            reaction_quantity = ceil(amout / reaction[0])

            ore_amout = reactions[element][1][0][1]
            total_costs += reaction_quantity * ore_amout

    return total_costs

if __name__ == "__main__":
    lines = open("input.txt", "r")
    for line in lines:
        [cost, outcome] = line.split("=>")

        (outcome_amout, outcome_element) = outcome.split()
        elements = [parse_element(element) for element in cost.strip().split(", ")]
        if len(elements) == 1 and elements[0][0] == "ORE":
            ore_reactions.append(outcome_element)

        reactions[outcome_element] = (int(outcome_amout), elements)
    print(f"Puzzle 1: {puzzle1()}")
