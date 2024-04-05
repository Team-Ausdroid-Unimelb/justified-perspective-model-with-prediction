(define 
        (problem coin2_tt_00039) 
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
                  (:epistemic $ b [a] (= (face-c) 'head'));;coin_maxd4_00001
                  (:epistemic - b [a] + b [b] - b [a] (= (face-c) 'head'));;coin_maxd4_00044
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    