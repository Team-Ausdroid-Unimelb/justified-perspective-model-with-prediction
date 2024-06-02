(define 
        (problem spcoin3_ttt_00007) 
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
                  (:epistemic + b [a] + b [b] + b [a] (= (face-c) 'head'));;spcoin_maxd4_00024
                  (:epistemic + b [b] + b [a] + b [b] + b [a] (= (face-c) 'head'));;spcoin_maxd4_00159
                  (:epistemic - b [b] - b [a] $ b [b] (= (face-c) 'head'));;spcoin_maxd4_00076
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    