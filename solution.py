assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r,cols) for r in rows]
column_units = [cross(rows,c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF','GHI') for cs in ('123','456','789')]
forward_diagonal = [rows[i] + cols[i] for i in range(len(rows))]
backward_diagonal = [rows[i] + cols[len(cols) - 1 - i] for i in range(len(rows))]
diagonal_units = [forward_diagonal, backward_diagonal]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    naked_twins_values = dict()

    # Iterate over each unit
    for unit in unitlist:
        unit_value_dict = dict()
        for box in unit:
            # Determine the value of each box and build out our key value dictionary
            box_value = values[box]
            if box_value in unit_value_dict.keys():
                unit_value_dict[box_value].append(box)
            else:
                unit_value_dict[box_value] = [box]
        for key, val in unit_value_dict.items():
            # If we trigger a naked twin
            if len(key) == 2 and len(val) == 2:
                if key in naked_twins_values.keys():
                    if val not in naked_twins_values[key]:
                        naked_twins_values[key].append(val)
                else:
                    naked_twins_values[key] = [val]
    for key, val in naked_twins_values.items():
        for naked_twin in val:
            # Find the intersection point relative to the two naked twins boxes' peers
            naked_twin_peers = peers[naked_twin[0]].intersection(peers[naked_twin[1]])
            single_peers = naked_twin_peers - set(naked_twin)
            # Iterate through each digit and determine if the value can be accepted
            # based on its peers. If eligible, assign the value
            for digit in key:
                for peer in single_peers:
                    if digit in values[peer]:
                        values = assign_value(values, peer, values[peer].replace(digit, ""))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes,chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    lines = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
        return values

def reduce_puzzle(values):
    solved_values_check = lambda value: len([box for box in values.keys() if len(values[box]) == value])
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False

    while not stalled:
        solved_values_before = solved_values_check(1)
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = solved_values_check(1)
        stalled = solved_values_before == solved_values_after
        if solved_values_check(0):
            return False
    return values

def search(values):
    # First reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve eah one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
