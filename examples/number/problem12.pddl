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
        (= (num c) 1)

        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;a learn the rule
        ;a know b learn the rule 
        ;both a and b did not see the number but know the value
        ; a dontknow bknow
        (= (:epistemic b [a] (= (num c) 11)) 1)
        (= (:epistemic b [b] (= (num c) 7)) 1)
        (= (:epistemic b [a] b [b] (= (num c) 7)) 1)
        ;(= (:ontic (= (peeking a) 'f')) 1)
        
    ))

    (:domains

        (peeking enumerate ['t','f'] static) ;
        (num integer [0,20] linear)
        ;static, linear, sin, 2nd_poly ###ax+b

    )       



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
