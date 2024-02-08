(define 
    (problem coin159) 
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
          (= (:epistemic b [a] b [b] (= (face c) 'head')) 0)
          (= (:epistemic b [b] (= (face c) 'head')) 0)
          (= (:epistemic b [b] b [a] (= (face c) 'head')) 1)
     ))

    (:domains
        (peeking enumerate ['t','f'])
        (face enumerate ['head','tail'])
    )
)
