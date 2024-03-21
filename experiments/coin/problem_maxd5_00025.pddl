(define 
        (problem coin_maxd5_00025) 
        (:domain coin)

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
          (:epistemic - b [a] + b [b] $ b [a] + b [b] - b [a] (= (face c) 'head')) 
          (:epistemic $ b [a] + b [b] $ b [a] - b [b] $ b [a] (= (face c) 'head')) 
          (:epistemic + b [b] - b [a] - b [b] - b [a] (= (face c) 'head')) 
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    