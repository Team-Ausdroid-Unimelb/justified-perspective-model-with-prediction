import os

class PDDL_Template:

    # this template is for separate looking coin
    problem_prefix1 ='''(define 
        (problem grapevine'''
    problem_prefix2 = ''') 
        (:domain grapevine)

        (:agents
            a b c d
        )
            
        (:objects
            p
        )

        (:variables
            (agent_at [a,b,c,d])
            (shared [a,b,c,d])
            (secret [a,b,c,d])
        )
    '''


    problem_init = '''
        (:init
            (= (agent_at a) 1)
            (= (agent_at b) 1)
            (= (agent_at c) 1)
            (= (agent_at d) 1)


            (= (shared a) 0)
            (= (shared b) 0)
            (= (shared c) 0)
            (= (shared d) 0)      

            ; constant dummy value to represent knows one's secret_at
            (= (secret a) 't')
            (= (secret b) 't')  
            (= (secret c) 't')  
            (= (secret d) 't')          
        )

    '''

    problem_goal_prefix = '''
        (:goal (and \n'''
    problem_goal_surfix = "     ))\n"


    problem_surfix = '''
        (:domains
            (agent_at integer [1,2])
            (shared integer [0,2])
            (secret enumerate ['t','f'])
        )
    )
    '''


    problem_path = os.path.join("experiments","grapevine")



    MAX_DEPTH = 5
    # this is a agent indifference domain

    agent_index_list = ["a","b","c","d"]
    # object_value_dict = {"(face c)":["'head'","'tail'"]}
    object_value_dict = \
        {"(secret a)":["'t'"],
         "(secret b)":["'t'"],
         "(secret c)":["'t'"],
        "(secret d)":["'t'"]}
    ternary_list = ['+','$','-']