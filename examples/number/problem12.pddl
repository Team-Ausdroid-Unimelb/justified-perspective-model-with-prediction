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

        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;a learn the rule
        ;a know b learn the rule 
        ;both a and b did not see the number but know the value
        (= (:epistemic b [a] (= (num c) 10)) 1)
        (= (:epistemic b [b] (= (num c) 10)) 1)
        (= (:epistemic b [a] b [b] (= (num c) 10)) 1)
        ;(= (:ontic (= (peeking a) 'f')) 1)
        
    ))

    (:domains

        (peeking enumerate ['t','f']) ;
        (num integer [0,20] linear)
        ;static, linear, sin, 2nd_poly ###ax+b

    )       



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
