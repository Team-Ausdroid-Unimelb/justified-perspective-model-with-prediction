import os



class PDDL_Template:
    # this template is for bbl
    problem_prefix1 ='''(define 
        (problem bbl'''
    problem_prefix2 = ''') 
        (:domain bbl)

        (:agents
            a b c d e f g h
        )
        (:objects 
            p
        )

        (:variables
            (dir [a,b,c,d,e,f,g,h])
            (x [a,b,c,d,e,f,g,h,p])
            (y [a,b,c,d,e,f,g,h,p])
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

            (= (x e) 3)
            (= (y e) 3)
            (= (dir e) 'n')

            (= (x f) 3)
            (= (y f) 3)
            (= (dir f) 'n')

            (= (x g) 3)
            (= (y g) 3)
            (= (dir g) 'n')

            (= (x h) 3)
            (= (y h) 3)
            (= (dir h) 'n')

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