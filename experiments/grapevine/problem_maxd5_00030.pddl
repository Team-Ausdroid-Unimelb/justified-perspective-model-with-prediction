(define 
        (problem grapevine_maxd5_00030) 
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
          (:epistemic + b [b] $ b [d] $ b [c] - b [b] $ b [a] (= (secret b) 't')) 
          (:epistemic $ b [d] - b [a] $ b [d] $ b [a] - b [c] (= (secret d) 't')) 
          (:epistemic $ b [c] + b [b] - b [c] + b [b] $ b [a] (= (secret c) 't')) 
          (:epistemic - b [d] - b [b] - b [d] - b [a] - b [b] (= (secret d) 't')) 
     ))

        (:domains
            (agent_at integer [1,2])
            (shared integer [0,2])
            (secret enumerate ['t','f'])
        )
    )
    