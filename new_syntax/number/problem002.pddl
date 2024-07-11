(define 
        (problem number_002) 
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
            (= (@ep ("+ b [a]") (= (num c) 17)) ep.true)
            (= (@ep ("+ b [b]") (= (num c) 17)) ep.true)
            )
        )

        (:ranges
            (peeking enumerate ['t','f'])
            (num integer [0,20])
        )

        (:rules
            (static (peeking a) [] [])
            (static (peeking b) [] [])
            (linear (num c) [2,1] [])
            ;(linear (num c) [2,1] [2,])  ;[,1]
        )
)