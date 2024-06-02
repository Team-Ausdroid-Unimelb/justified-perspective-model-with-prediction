import os


class PDDL_Template:

    # this template is for coin
    problem_prefix1 ='''(define 
        (problem sn'''
    problem_prefix2 = ''') 
        (:domain sn)

        (:agents
            a b c d
        )
            
        (:objects
            p1
        )

        (:variables
            (friended [a,b,c,d] [a,b,c,d])
            (post [p1] [a,b,c,d])
            (secret [p1])
            (nota [a,b,c,d])
        )
    '''

    problem_init = '''
        (:init
            (= (nota a) 0)
            (= (nota b) 1)
            (= (nota c) 1)
            (= (nota d) 1)

            (= (friended c a) 1)
            (= (friended c b) 1)
            (= (friended c c) 1)
            (= (friended c d) 1)
            
            (= (friended b a) 0)
            (= (friended b b) 1)
            (= (friended b c) 1)
            (= (friended b d) 0)
            
            (= (friended a a) 1)
            (= (friended a b) 0)
            (= (friended a c) 1)
            (= (friended a d) 1)
            
            (= (friended d a) 1)
            (= (friended d b) 0)
            (= (friended d c) 1)
            (= (friended d d) 1)
            
            (= (post p1 a) 0)
            (= (post p1 b) 0)
            (= (post p1 c) 0)
            (= (post p1 d) 0)

            (= (secret p1) 't')
        )
    '''

    problem_goal_prefix = '''
        (:goal (and \n'''
    problem_goal_surfix = "     ))\n"


    problem_surfix = '''
        (:domains
            (friended integer [0,1])
            (post integer [0,1])
            (nota integer [0,1])
            (secret enumerate ['t','f'])
        )
    )
    '''


    problem_path = os.path.join("experiments","sn")



    MAX_DEPTH = 3
    # this is a agent indifference domain

    agent_index_list = ["a","b","c","d"]
    # object_value_dict = {"(face c)":["'head'","'tail'"]}
    object_value_dict = {"(secret p1)":["'t'"]}
    
    ternary_list = ['+','$','-']