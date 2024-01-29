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
        (= (knows_rule a) 'yes') 
        (= (knows_rule b) 'yes') 
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;both a and b know rule
        ;cannot find different number if each have seen once
        (= (:epistemic b [a] (= (num c) 11)) 1)
        (= (:epistemic b [b] (= (num c) 13)) 1)
        
    ))

    (:domains

        (peeking enumerate ['t','f']) ;
        (num integer [0,20])
    ;static, linear, sin, 2nd_poly

 
        
           )  
) 