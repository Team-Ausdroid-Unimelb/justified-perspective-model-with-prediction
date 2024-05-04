(define 
        (problem bbl_a2_g3_ttt_00104) 
        (:domain bbl)

        (:agents
            a b c d
        )
        (:objects 
            p
        )

        (:variables
            (dir [a,b,c,d])
            (x [a,b,c,d,p])
            (y [a,b,c,d,p])
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

            (= (v p) 't')
        )
    
        (:goal (and 
          (:epistemic + b [a] (= (v-p) 't'))
          (:epistemic - b [a] $ b [b] $ b [a] $ b [b] (= (v-p) 't'))
          (:epistemic - b [a] + b [b] - b [a] (= (v-p) 't'))
     ))

        (:domains
            (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
            (x integer [0,4])
            (y integer [0,4])
            (v enumerate ['t','f'])
        )
    )
    