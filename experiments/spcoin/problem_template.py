import os

class PDDL_Template:

    # this template is for separate looking coin
    problem_prefix1 ='''(define 
        (problem spcoin'''
    problem_prefix2 = ''') 
        (:domain spcoin)

        (:agents
            a b
        )
        (:objects 
            c
        )

        (:variables
            (peeking [ a , b ])
            (face [c])
        )
    '''


    problem_init = '''
        (:init
            (= (peeking a) 'f')
            (= (peeking b) 'f')
            (= (face c) 'head')
        )
    '''

    problem_goal_prefix = '''
        (:goal (and \n'''
    problem_goal_surfix = "     ))\n"


    problem_surfix = '''
        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    '''


    problem_path = os.path.join("experiments","spcoin")



    MAX_DEPTH = 4
    # this is a agent indifference domain

    agent_index_list = ["a","b"]
    # object_value_dict = {"(face c)":["'head'","'tail'"]}
    object_value_dict = {"(face c)":["'head'"]}
    ternary_list = ['+','$','-']