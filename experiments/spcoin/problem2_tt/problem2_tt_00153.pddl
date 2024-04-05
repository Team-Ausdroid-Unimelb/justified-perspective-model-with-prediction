(define 
        (problem spcoin2_tt_00153) 
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
                  (:epistemic + b [b] - b [a] $ b [b] + b [a] (= (face-c) 'head'));;spcoin_maxd4_00180
                  (:epistemic + b [a] + b [b] $ b [a] (= (face-c) 'head'));;spcoin_maxd4_00025
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    