import os

# this template is for coin
problem_prefix1 ='''(define 
    (problem coin'''
problem_prefix2 = ''') 
    (:domain coin)

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


problem_path = os.path.join("experiments","coin")



DEPTH = 2
UNIFORM = True
UNIFORM = False
# this is a agent indifference domain

agent_index_list = ["a","b"]
# object_value_dict = {"(face c)":["'head'","'tail'"]}
object_value_dict = {"(face c)":["'head'"]}