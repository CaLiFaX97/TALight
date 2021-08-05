#!/bin/zsh 

PROBLEM=hanoi
SERVICE=check_one_sol

V=classic


GOAL=admissible
# GOAL=optimal
# GOAL=simple_walk
# GOAL=check_only_disk

# FEEDBACK=yes_no
# FEEDBACK=spot_first_non_optimal_move
FEEDBACK=gimme_shorter_solution
# FEEDBACK=gimme_optimal_solution

BOT_PATH="../bots/classic_hanoi_bot_check.py"
LANG=hardcoded
FORMAT=minimal


TEST=1
if [ $TEST = 1 ]; then
    START=all_A
    FINAL=all_C
    N=2
elif [ $TEST = 2 ]; then
    START=ABC
    FINAL=CBA
    N=-1
elif [ $TEST = 3 ]; then
    START=AABB
    FINAL=CBBA
    N=-1
elif [ $TEST = 4 ]; then
    START=all_A
    FINAL=all_C
    N=2
    LANG=it
    FORMAT=extended
elif [ $TEST = 5 ]; then
    START=all_A
    FINAL=all_C
    N=2
    LANG=en
    FORMAT=extended
fi



###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -av=$V \
    -aformat=$FORMAT \
    -agoal=$GOAL \
    -afeedback=$FEEDBACK \
    -alang=$LANG \
    -- $BOT_PATH