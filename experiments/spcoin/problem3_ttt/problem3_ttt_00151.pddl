(define 
        (problem spcoin3_ttt_00151) 
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
                  (:epistemic - b [b] + b [a] $ b [b] + b [a] (= (face-c) 'head'));;spcoin_maxd4_00216
                  (:epistemic - b [b] $ b [a] + b [b] - b [a] (= (face-c) 'head'));;spcoin_maxd4_00224
                  (:epistemic - b [b] + b [a] - b [b] - b [a] (= (face-c) 'head'));;spcoin_maxd4_00221
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    