( define 
    (problem coin_08) 
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
        (knows_rule [a , b])
    )

    (:init
        (= (peeking a) 'f')
        (= (peeking b) 'f')
        (= (face c) 'tail')
        (= (knows_rule a) 'yes') 
        (= (knows_rule b) 'yes') 
    )

    (:goal (and
        (= (:epistemic b [a] (= (face c) 'head')) 1)
        (= (:epistemic b [b] (= (face c) 'tail')) 1)
        (= (:epistemic b [b] b [a] (= (face c) 'head')) 1)
    ))

    (:domains
        (peeking enumerate ['t','f'])
        (face enumerate ['head','tail'])
        (knows_rule enumerate ['yes', 'no'])
    )

)