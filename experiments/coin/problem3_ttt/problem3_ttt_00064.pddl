(define 
        (problem coin3_ttt_00064) 
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
                  (:epistemic - b [b] + b [a] + b [b] - b [a] (= (face-c) 'head'));;coin_maxd4_00215
                  (:epistemic - b [b] $ b [a] $ b [b] $ b [a] (= (face-c) 'head'));;coin_maxd4_00226
                  (:epistemic + b [b] + b [a] + b [b] + b [a] (= (face-c) 'head'));;coin_maxd4_00159
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    