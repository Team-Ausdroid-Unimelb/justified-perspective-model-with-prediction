(define 
        (problem number_010) 
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
            (= (@ep ("+ b [a]") (= (num c) 9)) ep.true) ;7 have 9 no we both
            )
        )

        (:ranges
            (peeking enumerate ['t','f'])
            (num integer [-10,100])
        )

        (:rules
            (static (peeking a) [] [])
            (static (peeking b) [] [])
            (power (num c) [3] []);;,
        )
)