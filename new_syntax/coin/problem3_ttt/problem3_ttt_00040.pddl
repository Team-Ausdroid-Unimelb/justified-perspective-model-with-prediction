(define 
        (problem coin3_ttt_00040) 
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
                  (:epistemic - b [a] $ b [b] $ b [a] (= (face-c) 'head'));;coin_maxd4_00046
                  (:epistemic $ b [a] (= (face-c) 'head'));;coin_maxd4_00001
                  (:epistemic - b [b] + b [a] + b [b] $ b [a] (= (face-c) 'head'));;coin_maxd4_00214
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    