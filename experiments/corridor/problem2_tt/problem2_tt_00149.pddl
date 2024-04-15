(define 
        (problem corridor2_tt_00149) 
        (:domain corridor)

        (:agents
            a b c
        )
        (:objects 
            s
        )

        (:variables
            (agent_at [a,b,c])
            (secret_at [s])
            (sensed [s])
            (shared [s])
            (secret [s])
        )
    
        (:init
            (= (agent_at a) 1)
            (= (agent_at b) 2)
            (= (agent_at c) 3)
            (= (secret_at s) 2)
            (= (sensed s) 'f')
            (= (secret s) 't')
            ; the valid room is 1-4 only, zero means not done it yet
            (= (shared s) 0)
        )
    
        (:goal (and 
                  (:epistemic - b [a] + b [c] - b [b] + b [a] (= (secret-s) 't'));;corridor_maxd4_00957
                  (:epistemic - b [b] $ b [a] $ b [b] (= (secret-s) 't'));;corridor_maxd4_00250
     ))

        (:domains
            (agent_at integer [1,4])
            (secret_at integer [1,4])
            (shared integer [0,4])
            (sensed enumerate ['t','f'])
            (secret enumerate ['t','f'])
        )
    )
    