(define 
        (problem sn1_t_00236) 
        (:domain sn)

        (:agents
            a b c d
        )
            
        (:objects
            p1
        )

        (:variables
            (friended [a,b,c,d] [a,b,c,d])
            (post [p1] [a,b,c,d])
            (secret [p1])
            (nota [a,b,c,d])
        )
    
        (:init
            (= (nota a) 0)
            (= (nota b) 1)
            (= (nota c) 1)
            (= (nota d) 1)

            (= (friended c a) 1)
            (= (friended c b) 1)
            (= (friended c c) 1)
            (= (friended c d) 1)
            
            (= (friended b a) 0)
            (= (friended b b) 1)
            (= (friended b c) 1)
            (= (friended b d) 0)
            
            (= (friended a a) 1)
            (= (friended a b) 0)
            (= (friended a c) 1)
            (= (friended a d) 1)
            
            (= (friended d a) 1)
            (= (friended d b) 0)
            (= (friended d c) 1)
            (= (friended d d) 1)
            
            (= (post p1 a) 0)
            (= (post p1 b) 0)
            (= (post p1 c) 0)
            (= (post p1 d) 0)

            (= (secret p1) 't')
        )
    
        (:goal (and 
                  (:epistemic - b [b] + b [c] $ b [a] (= (secret-p1) 't'));;sn_maxd3_00553
     ))

        (:domains
            (friended integer [0,1])
            (post integer [0,1])
            (nota integer [0,1])
            (secret enumerate ['t','f'])
        )
    )
    