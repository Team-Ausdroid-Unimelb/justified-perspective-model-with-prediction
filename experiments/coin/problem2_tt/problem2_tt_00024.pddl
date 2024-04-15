(define 
        (problem coin2_tt_00024) 
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
                  (:epistemic - b [b] + b [a] + b [b] + b [a] (= (face-c) 'head'));;coin_maxd4_00213
                  (:epistemic + b [b] - b [a] - b [b] + b [a] (= (face-c) 'head'));;coin_maxd4_00183
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    