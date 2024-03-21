(define 
        (problem spcoin_maxd5_00023) 
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
          (:epistemic $ b [b] - b [a] + b [b] + b [a] - b [b] (= (face c) 'head')) 
          (:epistemic $ b [b] - b [a] - b [b] + b [a] (= (face c) 'head')) 
          (:epistemic $ b [a] - b [b] - b [a] $ b [b] + b [a] (= (face c) 'head')) 
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    