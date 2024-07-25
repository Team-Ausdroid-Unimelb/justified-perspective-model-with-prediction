(define 
        (problem number_005) 
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
            (= (@ep ("+ b [b] + b [a]") (= (num c) 3)) ep.true)
            (= (@ep ("+ b [b]") (= (num c) 11)) ep.true)
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