(define 
        (problem coin2_tt_00021) 
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
                  (:epistemic - b [b] $ b [a] - b [b] (= (face-c) 'head'));;coin_maxd4_00074
                  (:epistemic + b [a] + b [b] (= (face-c) 'head'));;coin_maxd4_00006
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    