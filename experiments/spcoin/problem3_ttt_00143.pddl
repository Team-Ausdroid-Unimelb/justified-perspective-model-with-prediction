(define 
        (problem spcoin3_ttt_00143) 
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
                  (:epistemic + b [a] + b [b] $ b [a] (= (face-c) 'head'));;spcoin_maxd4_00025
                  (:epistemic + b [b] - b [a] + b [b] + b [a] (= (face-c) 'head'));;spcoin_maxd4_00177
                  (:epistemic + b [a] + b [b] + b [a] (= (face-c) 'head'));;spcoin_maxd4_00024
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    