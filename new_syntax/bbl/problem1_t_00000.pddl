(define 
        (problem bbl1_t_00000) 
        (:domain bbl)

        (:agents
            a b - turnable
            c - locatable
        )
        (:objects 
            p - askable
        )

        (:init
            (assign (dir a) 'sw')
            (assign (dir b) 'n')
            (assign (x a) 3)
            (assign (x b) 2)
            (assign (x p) 1)
            (assign (y a) 3)
            (assign (y b) 2)
            (assign (y p) 1)
            (assign (v p) 't')
        )

        ; the @ represent this is an epistemic evaluation
        ; 
        (:goal 
            (and 
                (= (dir a) 'n')
                ; this representation is for return value from justified perspective function
                ; the range of the @jp depends on the variable
                ; (= (@jp ("+ b [b] + b [a]") (v-p)) 't')
                ; this representation is for evaluation of en epistemic formula with justified perspective model
                ; the range of the @ep has three possible value, ep.true, ep.unknown and ep.false
                ; (= (@ep ("+ b [b] + b [a]") (= (v-p) 1)) ep.true)
            )
        )

        ; D, domain of variables, in order to differentiate from the domain, we use range as key word
        (:ranges
            (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
            (x integer [0,4])
            (y integer [0,4])
            (v enumerate ['t','f'])
        )

        (:rules
            (static (dir a) [])
            (static (dir b) [])
            (static (dir p) [])
            (static (x a) [])
            (static (x b) [])
            (static (x p) [])
            (static (y a) [])
            (static (y b) [])
            (static (y p) [])
            (static (v p) [])
        )
    )