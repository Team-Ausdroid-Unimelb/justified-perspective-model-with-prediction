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
        (= (knows_rule b) 'no') 
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;no one know the rule but a guess b see 5
        (= (:epistemic b [a] (= (num c) 5)) 1)
        (= (:epistemic b [a] b [b] (= (num c) 5)) 1)
        (= (:ontic (= (peeking b) 'f')) 1)
        

        
    ))

    (:domains

        (peeking enumerate ['t','f']) ;
        (num integer [0,20])
    ;static, linear, sin, 2nd_poly

 
        
           )  
) 