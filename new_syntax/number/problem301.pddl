(define 
        (problem number_301) 
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
            (= (@ep ("+ b [a]") (= (num c) 37)) ep.true) ;7 have 9 no we both
            )
        )

        (:ranges
            (peeking enumerate ['t','f'])
            (num integer [0,40])
        )

        (:rules
            (static (peeking a) [] [])
            (static (peeking b) [] [])
            (2nd_poly (num c) [1,0,1] [,,])
        )
)