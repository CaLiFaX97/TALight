#!/usr/bin/env python3
from sys import stderr,stdout
from os import environ
from random import randrange, randint

from tc import TC

from functools import lru_cache

############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

MAPPER = {"tiny": 1, "small": 2, "medium": 3, "big": 4}
DATA = ((10, (5,6)), (10, (8,10)), (10, (18,20)), (70, (30,40)))
# that is, 10 instances of size "tiny", i.e., with 5 <= n <= 6 
#################################################################

def triangle_as_str(Tr):
    n = len(Tr)
    risp = str(Tr[0][0])
    for i in range(1,n):
        risp += "\n" + " ".join(map(str,Tr[i]))
    return risp

def display_triangle(Tr,out=stderr):
    print(triangle_as_str(Tr), file=out)
        
def max_val(Tr, r=0,c=0):
    #display_triangle(Tr,stderr)
    
    @lru_cache(maxsize=None)
    def max_val_ric_memo(r,c):
        assert 0 <= c <= r < n
        if r == n-1:
            #print(f"called with {r=},{c=} returns {Tr[r][c]=}", file=stderr)
            return Tr[r][c]
        risp = Tr[r][c] + max(max_val_ric_memo(r+1,c),max_val_ric_memo(r+1,c+1))
        #print(f"called with {r=},{c=} returns {risp=}", file=stderr)
        return risp

    n = len(Tr)
    return max_val_ric_memo(r,c)

def num_opt_sols(Tr, r=0,c=0):
    @lru_cache(maxsize=None)
    def num_opt_sols_ric_memo(r,c):
        assert 0 <= c <= r < n
        if r == n-1:
            return 1
        risp = 0
        if max_val(Tr, r,c) == Tr[r][c] + max_val(Tr, r+1,c):
            risp += num_opt_sols_ric_memo(r+1,c)
        if max_val(Tr, r,c) == Tr[r][c] + max_val(Tr, r+1,c+1):
            risp += num_opt_sols_ric_memo(r+1,c+1)
        return risp % 1000000007
    n = len(Tr)
    return num_opt_sols_ric_memo(r,c)

def opt_sol(Tr):
    n = len(Tr)
    sol = ""; r = 0; c = 0
    while r+1 < n:
        if max_val(Tr,r+1,c) >= max_val(Tr,r+1,c+1):
            sol += "L"; r += 1
        else:
            sol += "R"; r += 1; c += 1
    return sol

def unrank_safe(Tr,rnk):
    n = len(Tr)
    sol = ""; c = 0
    for r in range(n-1):
        #print(f"{r=}, {c=}, {rnk=}, num_opt_sols(Tr,r,c)",file=stderr)
        assert 0 <= rnk < num_opt_sols(Tr,r,c)
        if max_val(Tr, r,c) > Tr[r][c] + max_val(Tr,r+1,c):
            sol += "R"; c += 1
        else:
            assert max_val(Tr, r,c) == Tr[r][c]+max_val(Tr,r+1,c)
            if rnk < num_opt_sols(Tr,r+1,c):
                sol += "L"
            else:
                rnk -= num_opt_sols(Tr,r+1,c); sol += "R"; c += 1
    assert rnk == 0
    return sol

def rank_unsafe(Tr,sol,stated_opt_val):
    ok,val_of_sol = eval_sol_unsafe(Tr,sol)
    if not ok:
        return False,val_of_sol
    if stated_opt_val != val_of_sol:
        return False, f"On input:\n{triangle_as_str(Tr)}\nyou claimed that {stated_opt_val} is the optimum value of a solution. However, you then provided a solution whose value is {val_of_sol} rather then {stated_opt_val}.\nThe solution you have provided is:\n{sol}"
    opt_val = max_val(Tr)
    assert val_of_sol <= opt_val
    if val_of_sol < opt_val:
        return False, f"On input:\n{triangle_as_str(Tr)}\nyou claimed that {val_of_sol} is the optimal value. However, the optimal value is {opt_val}.\nIndeed, consider the following descending path:\n{opt_sol(Tr)}"
    n = len(Tr)
    rnk = 0; c = 0
    for r in range(n-1):
        if sol == "R" and max_val(Tr, r,c) == Tr[r][c]+max_val(Tr,r+1,c):
            rnk += num_opt_sols(Tr,r+1,c); c += 1
    return True,rnk

def eval_sol_unsafe(Tr,sol):
    n = len(Tr)
    if len(sol) != n-1:
        return False, f"Your solution:\n{sol}\n has length {len(sol)}. We were expecting a string of length {n-1=} over the alphabet {{'L','R'}} as the input triangle had {n=} rows."
    r = 0; c = 0
    val_sol = Tr[r][c]
    while r+1 < n:
        if sol[r] not in {'L','R'}:
            return False, f"Your solution:\n{sol}\n contains the character '{sol[r]}' in position {r} while we were expecting a string over the alphabet {{'L','R'}}."
        if sol[r] == 'R':
            c += 1
        r += 1
        val_sol += Tr[r][c]
    return True, val_sol

def gen_tc(min_n,max_n):
    n = randint(min_n, max_n)
    Tr = [[randint(0, 9) for j in range(i+1)] for i in range(n)]
    rnk = randrange(num_opt_sols(Tr))
    print(n,rnk)
    display_triangle(Tr,stdout)
    return (Tr,rnk)

def check_tc(Tr,rnk):
    risp_val = int(input())
    risp_sol = input().strip()
    ok, rank_of_risp = rank_unsafe(Tr,risp_sol,risp_val)
    if not ok:
        return False,rank_of_risp
    if rank_of_risp != rnk:
        return False, f"On input:\n{len(Tr)} {rnk}\n{triangle_as_str(Tr)}\nyou were right in stating that the optimum value of a solution is {risp_val}. However, you then returned the optimal solution:\n{risp_sol}\nwhich is of rank {rank_of_risp}. Instead, the optimal solution of rank {rnk}, as required, was:\n{unrank_safe(Tr,rnk)}"
    return True


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
