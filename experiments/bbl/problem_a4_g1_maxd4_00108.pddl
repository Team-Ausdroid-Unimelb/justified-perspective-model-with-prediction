(define 
        (problem bbl_a4_g1_maxd4_00108) 
        (:domain bbl)

        (:agents
            a b c d e f g h
        )
        (:objects 
            p
        )

        (:variables
            (dir [a,b,c,d,e,f,g,h])
            (x [a,b,c,d,e,f,g,h,p])
            (y [a,b,c,d,e,f,g,h,p])
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

            (= (x c) 3)
            (= (y c) 3)
            (= (dir c) 'n')

            (= (x d) 3)
            (= (y d) 3)
            (= (dir d) 'n')

            (= (x e) 3)
            (= (y e) 3)
            (= (dir e) 'n')

            (= (x f) 3)
            (= (y f) 3)
            (= (dir f) 'n')

            (= (x g) 3)
            (= (y g) 3)
            (= (dir g) 'n')

            (= (x h) 3)
            (= (y h) 3)
            (= (dir h) 'n')

            (= (v p) 't')
        )
    
        (:goal (and 
          (:epistemic $ b [a] + b [b] $ b [a] + b [b] (= (v-p) 't'))
     ))

        (:domains
            (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
            (x integer [0,4])
            (y integer [0,4])
            (v enumerate ['t','f'])
        )
    )
    