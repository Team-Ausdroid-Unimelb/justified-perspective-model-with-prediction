(define 
        (problem spcoin2_tt_00084) 
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
                  (:epistemic + b [b] + b [a] (= (face-c) 'head'));;spcoin_maxd4_00015
                  (:epistemic - b [b] + b [a] $ b [b] - b [a] (= (face-c) 'head'));;spcoin_maxd4_00218
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    