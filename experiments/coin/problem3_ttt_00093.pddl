(define 
        (problem coin3_ttt_00093) 
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
                  (:epistemic + b [a] - b [b] - b [a] + b [b] (= (face-c) 'head'));;coin_maxd4_00102
                  (:epistemic - b [b] - b [a] + b [b] $ b [a] (= (face-c) 'head'));;coin_maxd4_00232
                  (:epistemic + b [b] + b [a] + b [b] + b [a] (= (face-c) 'head'));;coin_maxd4_00159
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    