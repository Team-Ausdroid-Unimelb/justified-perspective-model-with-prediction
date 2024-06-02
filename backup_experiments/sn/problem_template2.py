import os


class PDDL_Template:

    # this template is for coin
    problem_prefix1 ='''(define 
        (problem sn'''
    problem_prefix2 = ''') 
        (:domain sn)

        (:agents
            a b c d e f g h
        )
            
        (:objects
            p1
        )

        (:variables
            (friended [a,b,c,d,e,f,g,h] [a,b,c,d,e,f,g,h])
            (post [p1] [a,b,c,d,e,f,g,h])
            (secret [p1])
            (nota [a,b,c,d,e,f,g,h])
        )
    '''

    problem_init = '''
        (:init
            (= (nota a) 0)
            (= (nota b) 1)
            (= (nota c) 1)
            (= (nota d) 1)
            (= (nota e) 1)
            (= (nota f) 1)
            (= (nota g) 1)
            (= (nota h) 1)
            

            (= (friended c a) 1)
            (= (friended c b) 1)
            (= (friended c c) 1)
            (= (friended c d) 1)
            (= (friended c e) 0)
            (= (friended c f) 0)
            (= (friended c g) 0)
            (= (friended c h) 0)
            
            (= (friended b a) 0)
            (= (friended b b) 1)
            (= (friended b c) 1)
            (= (friended b d) 0)
            (= (friended b e) 0)
            (= (friended b f) 0)
            (= (friended b g) 0)
            (= (friended b h) 0)
            
            (= (friended a a) 1)
            (= (friended a b) 0)
            (= (friended a c) 1)
            (= (friended a d) 1)
            (= (friended a e) 0)
            (= (friended a f) 0)
            (= (friended a g) 0)
            (= (friended a h) 0)
            
            (= (friended d a) 1)
            (= (friended d b) 0)
            (= (friended d c) 1)
            (= (friended d d) 1)
            (= (friended d e) 0)
            (= (friended d f) 0)
            (= (friended d g) 0)
            (= (friended d h) 0)

            (= (friended e a) 0)
            (= (friended e b) 0)
            (= (friended e c) 0)
            (= (friended e d) 0)
            (= (friended e e) 1)
            (= (friended e f) 0)
            (= (friended e g) 0)
            (= (friended e h) 0)

            (= (friended f a) 0)
            (= (friended f b) 0)
            (= (friended f c) 0)
            (= (friended f d) 0)
            (= (friended f e) 0)
            (= (friended f f) 1)
            (= (friended f g) 0)
            (= (friended f h) 0)

            (= (friended g a) 0)
            (= (friended g b) 0)
            (= (friended g c) 0)
            (= (friended g d) 0)
            (= (friended g e) 0)
            (= (friended g f) 0)
            (= (friended g g) 1)
            (= (friended g h) 0)

            (= (friended h a) 0)
            (= (friended h b) 0)
            (= (friended h c) 0)
            (= (friended h d) 0)
            (= (friended h e) 0)
            (= (friended h f) 0)
            (= (friended h g) 0)
            (= (friended h h) 1)
            


            (= (post p1 a) 0)
            (= (post p1 b) 0)
            (= (post p1 c) 0)
            (= (post p1 d) 0)

            (= (post p1 e) 0)
            (= (post p1 f) 0)
            (= (post p1 g) 0)
            (= (post p1 h) 0)

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