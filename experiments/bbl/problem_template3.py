import os



class PDDL_Template:
    # this template is for bbl
    problem_prefix1 ='''(define 
    (problem bbl'''
    problem_prefix2 = ''') 
    (:domain bbl)

    (:agents
        a b c - turnable
    )
    
    (:objects 
        p - askable
    )
    '''


    problem_init = '''
    (:init
        (assign (dir a) 'sw')
        (assign (dir b) 'n')
        (assign (x a) 3)
        (assign (x b) 2)
        (assign (x p) 1)
        (assign (y a) 3)
        (assign (y b) 2)
        (assign (y p) 1)
        (assign (v p) 't')
        (assign (dir c) 'e')
        (assign (x c) 0)
        (assign (y c) 0)
    )
    '''

    problem_goal_prefix = '''
    (:goal (and \n'''
    problem_goal_surfix = '''
        )
    )\n'''

    problem_surfix = '''
    (:ranges
        (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
        (x integer [0,4])
        (y integer [0,4])
        (v enumerate ['t','f'])
    )

    (:rules
        (static (dir a) [])
        (static (dir b) [])
        (static (dir p) [])
        (static (x a) [])
        (static (x b) [])
        (static (x p) [])
        (static (y a) [])
        (static (y b) [])
        (static (y p) [])
        (static (v p) [])
        (static (dir c) [])
        (static (x c) [])
        (static (y c) [])
    )
)
    '''


    # problem_path = os.path.join("experiments","bbl")



    MAX_DEPTH = 4
    # this is a agent indifference domain

    agent_index_list = ["a","b","c"]
    # object_value_dict = {"(face c)":["'head'","'tail'"]}
    object_value_dict = {"(v p)":["'t'"]}

    # the ternary list does not contain -1, which means false value does not make sense in BBL
    # because the the value of v is not changable
    ternary_list = ['+','$','!']