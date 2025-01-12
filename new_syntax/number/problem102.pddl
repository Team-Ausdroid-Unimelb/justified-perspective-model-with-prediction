(define 
        (problem number_102) 
        (:domain number01)

        (:agents
            a b - agent
        )

        (:objects
            c - num
        )

        (:init
            (assign (peeking a) 'f')
            (assign (peeking b) 'f')
            (assign (num c) 1)
        )


        (:goal 
            (and 
                ; solvable with prediction
                ; unsolvavle without prediction
                (= (@ep ("+ b [a]") (= (num c) 7)) ep.true) ;7 have 9 no we both
            )
        )

        (:ranges
            (peeking enumerate ['t','f'])
            (num integer [0,20])
        )

        (:rules
            (static (peeking a) [] [])
            (static (peeking b) [] [])
            (1st_poly (num c) [2,1] [,])
        )
)