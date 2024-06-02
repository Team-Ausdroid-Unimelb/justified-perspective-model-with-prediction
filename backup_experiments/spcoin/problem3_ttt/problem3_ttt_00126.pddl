(define 
        (problem spcoin3_ttt_00126) 
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
                  (:epistemic - b [b] $ b [a] - b [b] (= (face-c) 'head'));;spcoin_maxd4_00074
                  (:epistemic - b [a] + b [b] (= (face-c) 'head'));;spcoin_maxd4_00012
                  (:epistemic - b [a] - b [b] (= (face-c) 'head'));;spcoin_maxd4_00014
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    