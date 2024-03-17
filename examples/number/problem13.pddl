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
       
    )

    (:init
        (= (peeking a) 'f')
        (= (peeking b) 'f')
        (= (num c) 2)

        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;both a and b know rule
        ;cannot find different number if each have seen once
        (= (:epistemic b [a] (= (num c) 5)) 1)
        (= (:epistemic b [b] (= (num c) 9)) 1)
        
    ))

    (:domains

        (peeking enumerate ['t','f']) ;
        (num integer [0,20] linear)
    ;static, linear, sin, 2nd_poly

 
        
           )  
) 