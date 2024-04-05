(define 
        (problem spcoin3_ttt_00059) 
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
                  (:epistemic - b [b] - b [a] - b [b] - b [a] (= (face-c) 'head'));;spcoin_maxd4_00239
                  (:epistemic + b [a] + b [b] - b [a] - b [b] (= (face-c) 'head'));;spcoin_maxd4_00086
                  (:epistemic + b [b] - b [a] + b [b] - b [a] (= (face-c) 'head'));;spcoin_maxd4_00179
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    