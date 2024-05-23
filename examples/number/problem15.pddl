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
        (= (num 1) 2)

        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;a know the rule
        ;a dont know if b know the rule 
        ;no answer if b did not see at 5
        (= (:epistemic b [a] (= (num c) 7)) 1)
        (= (:epistemic b [a] b [b] (= (num c) 7)) 1)
        (= (:ontic (= (peeking a) 'f')) 1)
        

        
    ))

    (:domains

        (peeking enumerate ['t','f']) ;
        (num integer [0,20] linear)
        ;static, linear, sin, 2nd_poly

 
        
           )  
) 