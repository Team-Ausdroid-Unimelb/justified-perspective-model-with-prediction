(define 
        (problem spcoin3_ttt_00037) 
        (:domain spcoin)

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
                  (:epistemic + b [b] + b [a] + b [b] (= (face-c) 'head'));;spcoin_maxd4_00051
                  (:epistemic - b [a] $ b [b] $ b [a] + b [b] (= (face-c) 'head'));;spcoin_maxd4_00144
                  (:epistemic - b [a] $ b [b] + b [a] $ b [b] (= (face-c) 'head'));;spcoin_maxd4_00142
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    