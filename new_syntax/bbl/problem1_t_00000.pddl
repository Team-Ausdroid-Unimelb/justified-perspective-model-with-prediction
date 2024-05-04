(define 
        (problem bbl1_t_00000) 
        (:domain bbl)

        (:agents
            a b - turnable
        )
        (:objects 
            p - askable
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
    
        (:goal 
            (and 
               (= (@ "+ b [b] + b [a] (v-p)") 't')
            )
        )

        (:domains
            (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
            (x integer [0,4])
            (y integer [0,4])
            (v enumerate ['t','f'])
        )
    )
    