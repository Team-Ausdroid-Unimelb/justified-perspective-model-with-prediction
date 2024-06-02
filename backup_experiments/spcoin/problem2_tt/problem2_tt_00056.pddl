(define 
        (problem spcoin2_tt_00056) 
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
                  (:epistemic $ b [a] (= (face-c) 'head'));;spcoin_maxd4_00001
                  (:epistemic + b [a] (= (face-c) 'head'));;spcoin_maxd4_00000
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    