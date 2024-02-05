( define 
    (problem num_01) 
    (:domain number)

    (:agents
        a b
    )
    (:objects 
        c
    )

    (:variables
        (peeking [ a , b ])
        (num [c])
        (knows_rule [a , b])
    )

    (:init
        (= (peeking a) 'f')
        (= (peeking b) 'f')
        (= (num c) 2)
        (= (knows_rule a) 'no') 
        (= (knows_rule b) 'yes') 
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;a know the rule
        ;a dont know if b know the rule 
        ;no answer if b did not see at 5
        (= (:epistemic b [a] b [b] (= (num c) 3)) 1)
        (= (:epistemic b [b] (= (num c) 6)) 1)

        

        
    ))

    (:domains

        (peeking enumerate ['t','f']) ;
        (num integer [0,20])
        ;static, linear, sin, 2nd_poly

 
        
           )  
) 