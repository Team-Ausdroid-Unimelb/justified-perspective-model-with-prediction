(define 
        (problem spcoin3_ttt_00030) 
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
                  (:epistemic + b [a] - b [b] + b [a] $ b [b] (= (face-c) 'head'));;spcoin_maxd4_00097
                  (:epistemic - b [a] - b [b] $ b [a] (= (face-c) 'head'));;spcoin_maxd4_00049
                  (:epistemic - b [a] $ b [b] + b [a] - b [b] (= (face-c) 'head'));;spcoin_maxd4_00143
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    