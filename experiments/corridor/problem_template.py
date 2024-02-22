import os

# this template is for bbl
problem_prefix1 ='''(define 
    (problem corridor'''
problem_prefix2 = ''') 
    (:domain corridor)

    (:agents
        a b c
    )
    (:objects 
        s
    )

    (:variables
        (agent_at [a,b,c])
        (secret_at [s])
        (sensed [s])
        (shared [s])
        (secret [s])
    )
'''





problem_init = '''
    (:init
        (= (agent_at a) 1)
        (= (agent_at b) 2)
        (= (agent_at c) 3)
        (= (secret_at s) 2)
        (= (sensed s) 'f')
        (= (secret s) 't')
        ; the valid room is 1-4 only, zero means not done it yet
        (= (shared s) 0)
    )
'''

problem_goal_prefix = '''
    (:goal (and \n'''
problem_goal_surfix = "     ))\n"


problem_surfix = '''
    (:domains
        (agent_at integer [1,4])
        (secret_at integer [1,4])
        (shared integer [0,4])
        (sensed enumerate ['t','f'])
        (secret enumerate ['t','f'])
    )
)
'''


problem_path = os.path.join("experiments","corridor")



DEPTH = 1
UNIFORM = True
UNIFORM = False
# this is a agent indifference domain

agent_index_list = ["a","b","c"]
# object_value_dict = {"(face c)":["'head'","'tail'"]}
object_value_dict = {"(secret s)":["'t'"]}

# 262143