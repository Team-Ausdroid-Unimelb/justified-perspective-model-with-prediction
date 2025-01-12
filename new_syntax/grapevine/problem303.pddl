(define 
        (problem grapevine303) 
        (:domain grapevine)

        (:agents
            a b c - agent
        )
            
        (:objects
            sa sb sc - secret
            
        )

        (:init
            (assign (agent_loc a) 1)
            (assign (agent_loc b) 2)
            (assign (agent_loc c) 1)
            

            (assign (shared_loc sa) 0)
            (assign (shared_loc sb) 0)
            (assign (shared_loc sc) 0)
           

            (assign (own a sa) 1)
            (assign (own a sb) 0)
            (assign (own a sc) 0)
           

            (assign (own b sa) 0)
            (assign (own b sb) 1)
            (assign (own b sc) 0)
           

            (assign (own c sa) 0)
            (assign (own c sb) 0)
            (assign (own c sc) 1)
           

            (assign (sharing) 0)

            (assign (secret_truth_value sa) 2)
            (assign (secret_truth_value sb) 2)
            (assign (secret_truth_value sc) 2)
      

            (assign (agent_lyging_value a) 1)
            (assign (agent_lyging_value b) 1)
            (assign (agent_lyging_value c) 1)
          

            (assign (shared_value sa) 1)
            (assign (shared_value sb) 1)
            (assign (shared_value sc) 1)
     
        )

    
        (:goal (and 
                (= (@ep ("+ b [c]") (= (shared_value sa) 14)) ep.true)
                (= (@ep ("+ b [b]") (= (shared_value sa) 14)) ep.true)
                ;(= (@ep ("+ b [c] + b [b]") (= (shared_value sa) 13)) ep.false)
            )
        )

        (:ranges
            (agent_loc integer [1,2])
            (shared_loc integer [0,2])
            (own integer [0,1])
            (sharing integer [0,1])
            (secret_truth_value integer [0,15])
            (agent_lyging_value integer [0,15])
            (shared_value integer [0,15])
        )

        (:rules
            (static (agent_loc a) [] [])
            (static (agent_loc b) [] [])
            (static (agent_loc c) [] [])
            
            (static (shared_loc sa) [] [])
            (static (shared_loc sb) [] [])
            (static (shared_loc sc) [] [])
          
            (static (own a sa) [] [])
            (static (own a sb) [] [])
            (static (own a sc) [] [])
            
            (static (own b sa) [] [])
            (static (own b sb) [] [])
            (static (own b sc) [] [])
           
            (static (own c sa) [] [])
            (static (own c sb) [] [])
            (static (own c sc) [] [])
           
            (static (own d sa) [] [])
            (static (own d sb) [] [])
            (static (own d sc) [] [])
           
            (static (sharing) [] [])
            (1st_poly (secret_truth_value sa) [1,2] [,])
            (1st_poly (secret_truth_value sb) [1,2] [,])
            (1st_poly (secret_truth_value sc) [1,2] [,])
           
            (1st_poly (agent_lyging_value a) [1,1] [,])
            (1st_poly (agent_lyging_value b) [1,1] [,])
            (1st_poly (agent_lyging_value c) [1,1] [,])
          
            (1st_poly (shared_value sa) [1,2] [,])
            (1st_poly (shared_value sb) [1,2] [,])
            (1st_poly (shared_value sc) [1,2] [,])
        
            
        )
    )
    