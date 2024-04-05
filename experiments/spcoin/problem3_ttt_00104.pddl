(define 
        (problem spcoin3_ttt_00104) 
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
                  (:epistemic - b [a] - b [b] + b [a] - b [b] (= (face-c) 'head'));;spcoin_maxd4_00152
                  (:epistemic - b [a] + b [b] - b [a] $ b [b] (= (face-c) 'head'));;spcoin_maxd4_00139
                  (:epistemic + b [a] - b [b] - b [a] + b [b] (= (face-c) 'head'));;spcoin_maxd4_00102
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    