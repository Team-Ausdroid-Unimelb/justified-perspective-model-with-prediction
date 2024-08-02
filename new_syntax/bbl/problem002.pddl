(define 
        (problem bbl1_t_002) 
        (:domain bbl)

        (:agents
            a b c d - turnable
        )

        (:objects 
            p - askable
        )

        (:init
            (assign (dir a) 'ne')
            (assign (dir b) 'ne')
            (assign (dir c) 'n')
            (assign (dir d) 'e')
            (assign (x a) 1)
            (assign (x b) 2)
            (assign (x c) 2)
            (assign (x d) 0)
            (assign (x p) 0)
            (assign (y a) 1)
            (assign (y b) 2)
            (assign (y c) 0)
            (assign (y d) 2)
            (assign (y p) 0)
            (assign (v p) 't')
            (assign (actable a) 1)
            (assign (actable b) 0)
            (assign (actable c) 0)
            (assign (actable d) 0)
        )

        ; the @ represent this is an epistemic evaluation
        ; 
        (:goal 
            (and 
                ; solvable with prediction
                ; possiblly timeout
                (= (@ep ("+ b [a] + b [b] ") (= (v p) 't')) ep.true)
                (= (@ep ("+ b [a] + b [c] ") (= (v p) 't')) ep.true)
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
            (mod_1st (dir c) [] [])
            (mod_1st (dir d) [] [])
            (static (dir p) [] [])
            (static (x a) [] [])
            (static (x b) [] [])
            (static (x c) [] [])
            (static (x d) [] [])
            (static (x p) [] [])
            (static (y a) [] [])
            (static (y b) [] [])
            (static (y c) [] [])
            (static (y d) [] [])
            (static (y p) [] [])
            (static (v p) [] [])
            (static (actable a) [] [])
            (static (actable b) [] [])
            (static (actable c) [] [])
            (static (actable d) [] [])
        )
    )