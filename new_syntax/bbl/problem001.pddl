(define 
        (problem bbl1_t_001) 
        (:domain bbl)

        (:agents
            a b - turnable
        )

        (:objects 
            p - askable
        )

        (:init
            (assign (dir a) 'e')
            (assign (dir b) 'ne')
            (assign (x a) 1)
            (assign (x b) 2)
            (assign (x p) 0)
            (assign (y a) 1)
            (assign (y b) 2)
            (assign (y p) 0)
            (assign (v p) 't')
            (assign (actable a) 1)
            (assign (actable b) 0)
        )

        ; the @ represent this is an epistemic evaluation
        ; 
        (:goal 
            (and 
                (= (@ep ("+ b [a] + b [b] ") (= (v p) 't')) ep.true)
                ; (= (@ep ("+ b [b]") (= (v p) 't')) ep.true)
            )
        )

        ; D, domain of variables, in order to differentiate from the domain, we use range as key word
        (:ranges
            (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
            (x integer [0,4])
            (y integer [0,4])
            (v enumerate ['t','f'])
            (actable integer [0,1])
        )

        (:rules
            (static (dir a) [] [])
            (mod_1st (dir b) [] [])
            (static (dir p) [] [])
            (static (x a) [] [])
            (static (x b) [] [])
            (static (x p) [] [])
            (static (y a) [] [])
            (static (y b) [] [])
            (static (y p) [] [])
            (static (v p) [] [])
            (static (actable a) [] [])
            (static (actable b) [] [])
        )
    )