import os

class PDDL_Template:

    # this template is for bbl
    problem_prefix1 ='''(define 
        (problem corridor'''
    problem_prefix2 = ''') 
        (:domain corridor)

        (:agents
            a b c d e f g h i j k l
        )
        (:objects 
            s
        )

        (:variables
            (agent_at [a,b,c,d,e,f,g,h,i,j,k,l])
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
            (= (agent_at d) 3)
            (= (agent_at e) 3)
            (= (agent_at f) 3)
            (= (agent_at g) 3)
            (= (agent_at h) 3)
            (= (agent_at i) 3)
            (= (agent_at j) 3)
            (= (agent_at k) 3)
            (= (agent_at l) 3)
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



    MAX_DEPTH = 4
    UNIFORM = True
    UNIFORM = False
    # this is a agent indifference domain

    agent_index_list = ["a","b","c"]
    # object_value_dict = {"(face c)":["'head'","'tail'"]}
    object_value_dict = {"(secret s)":["'t'"]}
    
    ternary_list = ['+','$','-']

    # 262143