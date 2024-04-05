(define 
        (problem coin2_tt_00062) 
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
        )
    
        (:init
            (= (peeking a) 'f')
            (= (peeking b) 'f')
            (= (face c) 'head')
        )
    
        (:goal (and 
                  (:epistemic - b [b] - b [a] - b [b] + b [a] (= (face-c) 'head'));;coin_maxd4_00237
                  (:epistemic - b [b] $ b [a] + b [b] - b [a] (= (face-c) 'head'));;coin_maxd4_00224
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    