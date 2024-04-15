(define 
        (problem corridor3_ttt_00073) 
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
                  (:epistemic - b [c] - b [a] + b [b] $ b [c] (= (secret-s) 't'));;corridor_maxd4_02191
                  (:epistemic + b [a] + b [c] - b [a] - b [b] (= (secret-s) 't'));;corridor_maxd4_00509
                  (:epistemic - b [a] + b [b] + b [a] + b [b] (= (secret-s) 't'));;corridor_maxd4_00819
     ))

        (:domains
            (agent_at integer [1,4])
            (secret_at integer [1,4])
            (shared integer [0,4])
            (sensed enumerate ['t','f'])
            (secret enumerate ['t','f'])
        )
    )
    