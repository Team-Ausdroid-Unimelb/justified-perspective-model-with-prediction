(define 
        (problem coin009_000) 
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
          (= (:epistemic b [b] b [a] b [b] b [a] b [b] (= (face c) 'head')) -1) 
          (= (:epistemic b [a] b [b] b [a] b [b] b [a] (= (face c) 'head')) -1) 
     ))

        (:domains
            (peeking enumerate ['t','f'])
            (face enumerate ['head','tail'])
        )
    )
    