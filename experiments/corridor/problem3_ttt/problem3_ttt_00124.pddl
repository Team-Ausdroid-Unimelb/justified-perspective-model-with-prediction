(define 
        (problem corridor3_ttt_00124) 
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
                  (:epistemic + b [a] + b [c] - b [a] + b [c] (= (secret-s) 't'));;corridor_maxd4_00510
                  (:epistemic - b [c] $ b [a] $ b [c] + b [a] (= (secret-s) 't'));;corridor_maxd4_02175
                  (:epistemic + b [b] - b [a] $ b [b] $ b [c] (= (secret-s) 't'));;corridor_maxd4_01117
     ))

        (:domains
            (agent_at integer [1,4])
            (secret_at integer [1,4])
            (shared integer [0,4])
            (sensed enumerate ['t','f'])
            (secret enumerate ['t','f'])
        )
    )
    