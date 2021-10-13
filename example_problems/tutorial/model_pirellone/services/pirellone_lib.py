#!/usr/bin/env python3
"""This file contains the useful functions to handle 'Pirellone' Problem."""
import random, copy, re
from sys import exit


# CONSTANTS:
NO_SOL = 'NO SOLUTION'


# CONVERTERS FUNCTIONS:
def subset_to_seq(subset_sol):
    """Convert subset solution (e.g.: [[0,1],[0,0]]) into sequence solution (e.g.: ['r2'])"""
    if subset_sol == NO_SOL:
        return NO_SOL
    m = len(subset_sol[0])
    n = len(subset_sol[1])
    seq_sol = list()
    for i in range(m):
        if subset_sol[0][i]:
            seq_sol.append(f"r{i+1}")
    for j in range(n):
        if subset_sol[1][j]:
            seq_sol.append(f"c{j+1}")
    return seq_sol


def seq_to_subset(seq_sol, m, n):
    """Convert sequence solution (e.g.: ['r2']) into subset solution (e.g.: [[0,1],[0,0]])"""
    if seq_sol == NO_SOL:
        return NO_SOL
    assert isinstance(seq_sol, list)
    subset_sol = [[0]*m,[0]*n]
    for e in seq_sol:
        if e[0] == 'r':
            subset_sol[0][int(e[1:])-1] = (1-subset_sol[0][int(e[1:])-1])
        elif e[0] == 'c':
            subset_sol[1][int(e[1:])-1] = (1-subset_sol[1][int(e[1:])-1])
        else:
            raise RuntimeError(f'This seq_sol is bad written: {seq_sol}')
    return subset_sol


def parse_sol(raw_sol, sol_style, m, n):
    """Parse this raw_sol with sol_style and return the solution in correct format."""
    # Case0: general
    if len(raw_sol) > 2:
        raise RuntimeError('sol-bad-format')
    if (len(raw_sol) == 1) and (raw_sol == [NO_SOL]):
        return NO_SOL
    
    # Case1: sequence style
    sol = list()
    if sol_style == 'seq':
        if len(raw_sol) != 1:
            raise RuntimeError('sol-bad-format')
        # Checks no moves
        if raw_sol == ['']:
            return sol
        sol = raw_sol[0].split()
        for e in sol: 
            if any(not re.match("^((r|R|c|C)[1-9][0-9]*)$", e) for e in sol):
                raise RuntimeError('seq-regex', e)
            # Checks rows
            if (e[0] in ['r', 'R']) and (int(e[1:]) > m):
                raise RuntimeError('seq-row-m', e)
            # Checks cols
            if (e[0] in ['c', 'C']) and (int(e[1:]) > n):
                raise RuntimeError('seq-col-n', e)
        return sol
    
    # Case2: subset style
    elif sol_style == 'subset':
        # Check rows
        rows_switch = raw_sol[0].split()
        if len(rows_switch) != m:
            raise RuntimeError('subset-row-m', len(rows_switch))
        if any([not re.match(f"^(0|1)$", e) for e in rows_switch]):
            raise RuntimeError('subset-regex', raw_sol[0])
        sol.append([int(e) for e in rows_switch])
        # Check cols
        cols_switch = raw_sol[1].split()
        if len(cols_switch) != n:
            raise RuntimeError('subset-col-n', len(cols_switch))
        if any([not re.match(f"^(0|1)$", e) for e in cols_switch]):
            raise RuntimeError('subset-regex', raw_sol[1])
        sol.append([int(e) for e in cols_switch])
        return sol
    
    # Case3: invalid style
    else:
        raise RuntimeError('invalid-sol-style')


# TO_STRING and FROM_STRING FUNCTIONS:
def seq_to_str(seq_sol):
    """From a sequence solution (e.g.: ['r2']) returns its string form (e.g.: 'r2')"""
    if seq_sol == NO_SOL:
        return NO_SOL
    return ' '.join(seq_sol)


def sol_to_str(pirellone, subset_sol):
    """Print the pirellone instance with the rows and cols to be switches"""
    m = len(pirellone)
    n = len(pirellone[0])
    if subset_sol == NO_SOL:
        sol_str =  f'    {"? " * n}'
        sol_str = sol_str[:-1] + '\n'
        sol_str += f'    {"-" * ((m*2)-1)}\n'
        for i in range(m):
            sol_str += f'? | '
            sol_str += ' '.join(str(e) for e in pirellone[i]) + '\n'
    else:
        sol_str = '    ' + ' '.join(str(e) for e in subset_sol[1]) + '\n'
        sol_str += f'    {"-" * (len(subset_sol[1]*2)-1)}\n'
        for i in range(m):
            sol_str += f'{subset_sol[0][i]} | '
            sol_str += ' '.join(str(e) for e in pirellone[i]) + '\n'
    return sol_str[:-1]


def subset_to_str(subset_sol):
    sol = subset_to_str_list(subset_sol)
    if sol == NO_SOL:
        return NO_SOL
    return sol[0] + '\n' + sol[1]


def subset_to_str_list(subset_sol):
    """From a subset solution (e.g.: [[0,1],[0,0]]) returns a list with the rows string and the columns string (e.g.: ['0 1', '0 0']) or NO_SOL"""
    if subset_sol == NO_SOL:
        return NO_SOL
    return [' '.join([str(e) for e in subset_sol[0]]), \
            ' '.join([str(e) for e in subset_sol[1]])]


def get_pirellone_from_str(str):
    """From a string, this function returns a pirellone instance in list form."""
    pirellone = list()
    rows = str.split('\n')
    for cols in rows:
        pirellone.append([int(e) for e in cols.split()])
    return pirellone


def pirellone_to_str(pirellone):
    """From a pirellone instance, this function returns its string rappresentation."""
    return '\n'.join((' '.join(str(col) for col in row) for row in pirellone))


# PIRELLONE GENERATOR FUNCTIONS:
def is_solvable_seed(seed):
    """If this seed is associated to a solvable pirellone instance return True, False otherwise."""
    # We reserve those seed divisible by 3 to the NOT solvable instances
    return (seed % 3) != 0


def gen_pirellone_seed(solvable=None):
    """This function returns a seed to generate a pirellone instance with the specificated solvability."""
    random.seed()
    seed = random.randint(100002,999999)
    # Check solvability
    if solvable == None:
        solvable = random.choice([False, True])
    # adust seed if not suitable
    if solvable != is_solvable_seed(seed):
        # We reserve those seed divisible by 3 to the NOT solvable instances
        if solvable:
            seed -= random.randrange(1, 3)   
        else:
            seed -= (seed % 3)  
    return seed


def gen_pirellone(m, n, seed, with_yes_certificate=False):
    """From (m,n,seed), this functions returns a pirellone instance, with eventually the certificate."""
    assert m >= 0
    assert n >= 0
    solvable = is_solvable_seed(seed)
    # Generate pirellone
    random.seed(seed)
    switches_row = [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]
    if not solvable:
        if m < 2 or n < 2:
            # In this case, the pirellone is always solvable
            raise RuntimeError('invalid-unsolvable-dimensions')
        num_altered_rows = random.randrange(1, m)
        altered_rows= random.sample(range(m), num_altered_rows)
        for row in altered_rows:
            col = random.randrange(0, n)
            pirellone[row][col] = 1 - pirellone[row][col] 
    if with_yes_certificate:
        return pirellone, switches_row, switches_col
    else:
        return pirellone


# GET_SOL FUNCTIONS:
def get_opt_sol_from_solution(switches_row: List[int], switches_col: List[int]):
    """Returns the optimal solution of a solvable pirellone given a first solution."""
    m = len(switches_row)
    n = len(switches_col)
    if sum(switches_col) + sum(switches_row) > (m+n)//2:
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    return [switches_row, switches_col]

def get_opt_sol_if_solvable(pirellone: List[List[int]]):
    """Returns the optimal solution of a solvable pirellone."""
    m = len(pirellone)
    n = len(pirellone[0])
    switches_col = pirellone[0]
    if switches_col[0]:
       switches_row = [ pirellone[_][0] for _ in range(m) ]
    else:
       switches_row = [ 1-pirellone[_][0] for _ in range(m) ]
    return get_opt_sol_from(switches_row,switches_col)

def check_sol(pirellone: List[List[int]], sol, sol_style):
    """returns True if sol turns off entirely the pirellone. Otherwise it returns False and an (i,j) such that pirellone[i,j] is set to one after the solution sol gets applied."""
    assert sol != NO_SOL
    m = len(pirellone)
    n = len(pirellone[0])
    if sol_style == "seq":
        sol = seq_to_subset(sol,m,n)
    switches_row, switches_col = sol
    for i in range(m):
        for j in range(n):
            if pirellone[i][j] != (switches_row[i] + switches_col[j])%2:
                return False, (i,j)
    return True, None


def sol_is_the_min(m, n, sol, sol_style):
    """It assumes that sol contains a valid solution. Returns True if this solution is the minimum one"""
    assert sol != NO_SOL
    if sol_style == "seq":
        sol = seq_to_subset(sol,m,n)
    switches_row, switches_col = sol
    return sum(switches_col)+sum(switches_row) <= (m+n)//2


def is_solvable(pirellone: List[List[int]]) -> bool:
    """From a pirellone instance, this functions returns True if it is solvable, False otherwise."""
    return check_sol(pirellone, get_opt_sol_if_solvable(pirellone))



def get_padded_sol(m:int, n:int, seq_sol:List[str], pad_size:int):
    """From (m,n) and a sequence solution (e.g.: ['r2']), this functions returns a solution longer than at least pad_size."""
    if seq_sol == NO_SOL:
        return NO_SOL
    assert isinstance(seq_sol, list) and all(isinstance(e, str) for e in seq_sol)
    padded_sol = seq_sol.copy()
    diff = pad_size
    turn = 0
    while diff > 0:
        if turn == 0:
            # add fake random row move
            num = f"r{random.randint(1, m)}"
        else:
            # add fake random col move
            num = f"c{random.randint(1, n)}"
        padded_sol.append(num)
        padded_sol.append(num)
        turn = (turn + 1) % 2
        diff -= 2
    random.shuffle(padded_sol)
    return padded_sol





# TESTS
if __name__ == "__main__":

    print('Test: subset_to_seq()')
    assert subset_to_seq([[0, 0, 1], [0, 1, 0]]) == ['r3', 'c2']
    assert subset_to_seq(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: seq_to_subset()')
    assert seq_to_subset(['r3', 'c2'], 4, 4) == [[0, 0, 1, 0], [0, 1, 0, 0]]
    print(seq_to_subset(['r1', 'c2', 'c2'], 3, 3))
    assert seq_to_subset(['r1', 'c2', 'c2'], 3, 3) == [[1, 0, 0], [0, 0, 0]]
    assert seq_to_subset(NO_SOL, 4, 4) == NO_SOL
    print('==> OK\n')


    print('Test: parse_sol()')
    # import model_utils as mu
    # raw_sol = mu.get_raw_solution()
    # print(f'raw_sol: {raw_sol}')
    assert parse_sol([NO_SOL], 'seq', 2, 2) == NO_SOL
    assert parse_sol([NO_SOL], 'subset', 2, 2) == NO_SOL
    assert parse_sol(['1 0 1 0 0 ', '0 1 0 0 1 '], 'subset', 5, 5) == \
        [[1, 0, 1, 0, 0], [0, 1, 0, 0, 1]]
    assert parse_sol([''], 'seq', 2, 2) == []
    assert parse_sol(['r1 r2 c2'], 'seq', 2, 2) == ['r1', 'r2', 'c2']
    print('==> OK\n')


    print('Test: seq_to_str()')
    assert seq_to_str(['r3', 'c2']) == 'r3 c2'
    assert seq_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: sol_to_str()')
    assert sol_to_str([[0, 0], [1, 1]], [[0, 1], [0, 0]]) == \
        "    0 0\n" + \
        "    ---\n" + \
        "0 | 0 0\n" + \
        "1 | 1 1"
    print(sol_to_str([[0, 0], [0, 1]], NO_SOL))
    assert sol_to_str([[0, 0], [0, 1]], NO_SOL) == \
        "    ? ?\n" + \
        "    ---\n" + \
        "? | 0 0\n" + \
        "? | 0 1"
    print('==> OK\n')


    print('Test: subset_to_str()')
    assert subset_to_str([[0, 0, 1], [0, 1, 0]]) == "0 0 1\n0 1 0"
    assert subset_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: subset_to_str_list()')
    assert subset_to_str_list([[0, 0, 1], [0, 1, 0]]) == ['0 0 1', '0 1 0']
    assert subset_to_str_list(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: pirellone_to_str()')
    assert pirellone_to_str([[0, 0], [1, 1]]) == '0 0\n1 1'
    print('==> OK\n')


    print('Test: get_pirellone_from_str()')
    assert get_pirellone_from_str('0 0\n1 1') == [[0, 0], [1, 1]]
    print('==> OK\n')


    print('Test: is_solvable_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_pirellone_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_pirellone()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: get_opt_sol_from()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: get_opt_sol() in solvable instances')
    assert get_opt_sol([[0, 0], [0, 0]]) == [[0, 0],[0, 0]]
    assert get_opt_sol([[0, 0], [1, 1]]) == [[0, 1],[0, 0]]
    assert get_opt_sol([[0, 1], [0, 1]]) == [[0, 0],[0, 1]]
    assert get_opt_sol([[0, 1], [1, 0]]) in [[[1, 0],[1, 0]],
                                             [[0, 1],[0, 1]]]
    assert get_opt_sol([[1, 0], [0, 1]]) in [[[1, 0],[0, 1]],
                                             [[0, 1],[1, 0]]]
    assert get_opt_sol([[1, 0], [1, 0]]) == [[0, 0],[1, 0]]
    assert get_opt_sol([[1, 1], [0, 0]]) == [[1, 0],[0, 0]]
    assert get_opt_sol([[1, 1], [1, 1]]) in [[[1, 1],[0, 0]],
                                             [[0, 0],[1, 1]]]
    print('Test: get_opt_sol() in NOT solvable instances')
    print('THIS BEHAVIOR HAS YET TO BE IMPLEMENTATED')
    # assert get_opt_sol([[0, 0], [0, 1]]) == NO_SOL
    # assert get_opt_sol([[0, 0], [1, 0]]) == NO_SOL
    # assert get_opt_sol([[0, 1], [0, 0]]) == NO_SOL
    # assert get_opt_sol([[0, 1], [1, 1]]) == NO_SOL
    # assert get_opt_sol([[1, 0], [0, 0]]) == NO_SOL
    # assert get_opt_sol([[1, 0], [1, 1]]) == NO_SOL
    # assert get_opt_sol([[1, 1], [0, 1]]) == NO_SOL
    # assert get_opt_sol([[1, 1], [1, 0]]) == NO_SOL
    print('==> OK\n')


    print('Test: switch_row()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: switch_col()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: are_equiv()')
    assert are_equiv([[0, 0], [0, 1]], [[0, 0], [0, 1]])
    assert are_equiv(NO_SOL, NO_SOL)
    assert are_equiv([[0, 0], [0, 1]], [[1, 1], [1, 0]])
    assert are_equiv([[1, 0], [0, 1]], [[0, 1], [1, 0]])
    assert not are_equiv([[0, 0], [0, 1]], NO_SOL)
    assert not are_equiv(NO_SOL, [[0, 0], [0, 1]])
    assert not are_equiv([[0, 0], [0, 1]], [[0, 0], [1, 0]])
    print('==> OK\n')


    print('Test: is_solvable() in solvable instances')
    assert is_solvable([[0, 0], [0, 0]])
    assert is_solvable([[0, 0], [1, 1]])
    assert is_solvable([[0, 1], [0, 1]])
    assert is_solvable([[0, 1], [1, 0]])
    assert is_solvable([[1, 0], [0, 1]])
    assert is_solvable([[1, 0], [1, 0]])
    assert is_solvable([[1, 1], [0, 0]])
    assert is_solvable([[1, 1], [1, 1]])
    print('==> OK\n')
    print('Test: is_solvable() in NOT solvable instances')
    assert not is_solvable([[0, 0], [0, 1]])
    assert not is_solvable([[0, 0], [1, 0]])
    assert not is_solvable([[0, 1], [0, 0]])
    assert not is_solvable([[0, 1], [1, 1]])
    assert not is_solvable([[1, 0], [0, 0]])
    assert not is_solvable([[1, 0], [1, 1]])
    assert not is_solvable([[1, 1], [0, 1]])
    assert not is_solvable([[1, 1], [1, 0]])
    print('==> OK\n')


    print('Test: get_padded_sol_seq()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: get_light_on_after() in solvable instances')
    assert get_light_on_after([[0, 0], [0, 0]], get_opt_sol([[0, 0], [0, 0]])) == 0
    assert get_light_on_after([[0, 0], [1, 1]], get_opt_sol([[0, 0], [1, 1]])) == 0
    assert get_light_on_after([[0, 1], [0, 1]], get_opt_sol([[0, 1], [0, 1]])) == 0
    assert get_light_on_after([[0, 1], [1, 0]], get_opt_sol([[0, 1], [1, 0]])) == 0
    assert get_light_on_after([[1, 0], [0, 1]], get_opt_sol([[1, 0], [0, 1]])) == 0
    assert get_light_on_after([[1, 0], [1, 0]], get_opt_sol([[1, 0], [1, 0]])) == 0
    assert get_light_on_after([[1, 1], [0, 0]], get_opt_sol([[1, 1], [0, 0]])) == 0
    assert get_light_on_after([[1, 1], [1, 1]], get_opt_sol([[1, 1], [1, 1]])) == 0
    assert get_light_on_after([[1, 1], [1, 1]], [[0, 0], [0, 0]]) == 4
    assert get_light_on_after([[1, 1], [1, 1]], [[1, 0], [0, 0]]) == 2
    assert get_light_on_after([[1, 1], [1, 1]], [[1, 1], [0, 0]]) == 0
    print('==> OK\n')
    print('Test: check_off_lights() in NOT solvable instances')
    assert not get_light_on_after([[0, 0], [0, 1]], get_opt_sol([[0, 0], [0, 1]])) == None
    assert not get_light_on_after([[0, 0], [1, 0]], get_opt_sol([[0, 0], [1, 0]])) == None
    assert not get_light_on_after([[0, 1], [0, 0]], get_opt_sol([[0, 1], [0, 0]])) == None
    assert not get_light_on_after([[0, 1], [1, 1]], get_opt_sol([[0, 1], [1, 1]])) == None
    assert not get_light_on_after([[1, 0], [0, 0]], get_opt_sol([[1, 0], [0, 0]])) == None
    assert not get_light_on_after([[1, 0], [1, 1]], get_opt_sol([[1, 0], [1, 1]])) == None
    assert not get_light_on_after([[1, 1], [0, 1]], get_opt_sol([[1, 1], [0, 1]])) == None
    assert not get_light_on_after([[1, 1], [1, 0]], get_opt_sol([[1, 1], [1, 0]])) == None


    print('Test: get_min_lights_on() in solvable instances')
    # assert get_min_lights_on([[0, 0], [0, 0]]) == 0
    # assert get_min_lights_on([[0, 0], [1, 1]]) == 0
    # assert get_min_lights_on([[0, 1], [0, 1]]) == 0
    # assert get_min_lights_on([[0, 1], [1, 0]]) == 0
    # assert get_min_lights_on([[1, 0], [0, 1]]) == 0
    # assert get_min_lights_on([[1, 0], [1, 0]]) == 0
    # assert get_min_lights_on([[1, 1], [0, 0]]) == 0
    # assert get_min_lights_on([[1, 1], [1, 1]]) == 0
    print('THIS BEHAVIOR HAS YET TO BE IMPLEMENTATED')
    print('==> OK\n')
    print('Test: get_min_lights_on() in NOT solvable instances')
    print('THIS BEHAVIOR HAS YET TO BE IMPLEMENTATED')
    print('==> OK\n')

