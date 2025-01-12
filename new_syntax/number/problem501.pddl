(define 
        (problem number_501) 
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
            (assign (num c) 0)
        )


        (:goal 
            (and 
            (= (@ep ("+ b [a]") (= (num c) 0)) ep.true) 
            )
        )

        (:ranges
            (peeking enumerate ['t','f'])
            (num integer [-10,10])
        )

        (:rules
            (static (peeking a) [] [])
            (static (peeking b) [] [])
            (sin (num c) [8,1,0] [,,])
        )
)