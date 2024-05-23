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
        ;both a and b learn the rule
        ;both a and b did not see the number but know the value
        (= (:epistemic b [a] (= (num c) 11)) 1)
        (= (:epistemic b [b] (= (num c) 11)) 1)
        ;(= (:ontic (= (peeking b) 'f')) 1)
        ;(= (:ontic (= (peeking a) 'f')) 1)  
    ))

    (:domains

        (peeking enumerate ['t','f']) ;
        (num integer [0,20] linear)
    ;static, linear, sin, 2nd_poly

    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
