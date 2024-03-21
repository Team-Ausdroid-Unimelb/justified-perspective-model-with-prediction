(define 
        (problem grapevine_maxd3_00218) 
        (:domain grapevine)

        (:agents
            a b c d
        )
            
        (:objects
            p
        )

        (:variables
            (agent_at [a,b,c,d])
            (shared [a,b,c,d])
            (secret [a,b,c,d])
        )
    
        (:init
            (= (agent_at a) 1)
            (= (agent_at b) 1)
            (= (agent_at c) 1)
            (= (agent_at d) 1)


            (= (shared a) 0)
            (= (shared b) 0)
            (= (shared c) 0)
            (= (shared d) 0)      

            ; constant dummy value to represent knows one's secret_at
            (= (secret a) 't')
            (= (secret b) 't')  
            (= (secret c) 't')  
            (= (secret d) 't')          
        )

    
        (:goal (and 
          (:epistemic $ b [a] $ b [b] - b [d] (= (secret a) 't')) 
     ))

        (:domains
            (agent_at integer [1,2])
            (shared integer [0,2])
            (secret enumerate ['t','f'])
        )
    )
    