import os



class PDDL_Template:
    # this template is for bbl
    problem_prefix1 ='''(define 
        (problem bbl'''
    problem_prefix2 = ''') 
        (:domain bbl)

        (:agents
            a b c d
        )
        (:objects 
            p
        )

        (:variables
            (dir [a,b,c,d])
            (x [a,b,c,d,p])
            (y [a,b,c,d,p])
            (v [p])
        )
    '''


    problem_init = '''
        (:init
            (= (dir a) 'sw')
            (= (dir b) 'n')
            (= (x a) 3)
            (= (x b) 2)
            (= (x p) 1)
            (= (y a) 3)
            (= (y b) 2)
            (= (y p) 1)

            (= (x c) 3)
            (= (y c) 3)
            (= (dir c) 'n')

            (= (x d) 3)
            (= (y d) 3)
            (= (dir d) 'n')

            (= (v p) 't')
        )
    '''

    problem_goal_prefix = '''
        (:goal (and \n'''
    problem_goal_surfix = "     ))\n"


    problem_surfix = '''
        (:domains
            (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
            (x integer [0,4])
            (y integer [0,4])
            (v enumerate ['t','f'])
        )
    )
    '''


    problem_path = os.path.join("experiments","bbl")



    MAX_DEPTH = 4
    # this is a agent indifference domain

    agent_index_list = ["a","b"]
    # object_value_dict = {"(face c)":["'head'","'tail'"]}
    object_value_dict = {"(v p)":["'t'"]}

    # the ternary list does not contain -1, which means false value does not make sense in BBL
    # because the the value of v is not changable
    ternary_list = ['+','$','-']