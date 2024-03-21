(define 
        (problem bbl_maxd4_00131) 
        (:domain bbl)

        (:agents
            a b
        )
        (:objects 
            p
        )

        (:variables
            (dir [ a , b ])
            (x [a,b,p])
            (y [a,b,p])
            (v [p])
        )
    
        (:init
            (= (dir a) 'sw')
            (= (dir b) 'n')
            (= (x a) 3)
            (= (x b) 2)
            (= (x p) 1)
            (= (y a) 3)
            (= (y b) 2)
            (= (y p) 1)
            (= (v p) 't')
        )
    
        (:goal (and 
          (:epistemic $ b [a] - b [b] - b [a] - b [b] (= (v p) 't')) 
     ))

        (:domains
            (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
            (x integer [0,4])
            (y integer [0,4])
            (v enumerate ['t','f'])
        )
    )
    