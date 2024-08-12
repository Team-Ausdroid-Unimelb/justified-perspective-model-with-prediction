(define 
        (problem grapevine000) 
        (:domain grapevine)
        
        (:agents
            a b - agent
        )
        (:objects
            as bs - secret
        )

        (:init
            (assign (agent_loc a) 1)
            (assign (agent_loc b) 1)
            (assign (shared_loc as) 0)
            (assign (shared_loc bs) 0)
            (assign (own a as) 1)
            (assign (own a bs) 0)
            (assign (own b as) 0)
            (assign (own b bs) 1)
            (assign (sharing) 0)
            (assign (secret_value as) 2)
            (assign (secret_value bs) 2)
            (assign (secret_lyging_value as) 1)
            (assign (secret_lyging_value bs) 1)
            (assign (shared_value as) 2)
            (assign (shared_value bs) 2)
        )

    
        (:goal (and 
                (= (@ep ("+ b [b]") (= (shared_value as) 6)) ep.true)
            )
        )

        (:ranges
            (agent_loc integer [1,2])
            (shared_loc integer [0,2])
            (own integer [0,1])
            (sharing integer [0,1])
            (secret_value integer [0,9])
            (secret_lyging_value integer [0,9])
            (shared_value integer [0,9])
        )

        (:rules
            (static (agent_loc a) [] [])
            (static (agent_loc b) [] [])
            (static (shared_loc as) [] [])
            (static (shared_loc bs) [] [])
            (static (own a as) [] [])
            (static (own a bs) [] [])
            (static (own b as) [] [])
            (static (own b bs) [] [])
            (static (sharing) [] [])
            (1st_poly (secret_value as) [1,2] [,])
            (1st_poly (secret_value bs) [1,2] [,])
            (static (secret_lyging_value as) [] [])
            (static (secret_lyging_value bs) [] [])
            (1st_poly (shared_value as) [1,2] [,])
            (1st_poly (shared_value bs) [1,2] [,])
        )
    )
    