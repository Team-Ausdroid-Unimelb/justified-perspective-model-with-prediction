(define 
        (problem grapevine003) 
        (:domain grapevine)

        (:agents
            a b c d - agent
        )
            
        (:objects
            as bs cs ds - secret
            
        )

        (:init
            (assign (agent_loc a) 1)
            (assign (agent_loc b) 1)
            (assign (agent_loc c) 1)
            (assign (agent_loc d) 1)

            (assign (shared_loc as) 0)
            (assign (shared_loc bs) 0)
            (assign (shared_loc cs) 0)
            (assign (shared_loc ds) 0)

            (assign (own a as) 1)
            (assign (own a bs) 0)
            (assign (own a cs) 0)
            (assign (own a ds) 0)

            (assign (own b as) 0)
            (assign (own b bs) 1)
            (assign (own b cs) 0)
            (assign (own b ds) 0)

            (assign (own c as) 0)
            (assign (own c bs) 0)
            (assign (own c cs) 1)
            (assign (own c ds) 0)

            (assign (own d as) 0)
            (assign (own d bs) 0)
            (assign (own d cs) 0)
            (assign (own d ds) 1)

            (assign (sharing) 0)

            (assign (secret_value as) 2)
            (assign (secret_value bs) 2)
            (assign (secret_value cs) 2)
            (assign (secret_value ds) 2)

            (assign (secret_lyging_value as) 1)
            (assign (secret_lyging_value bs) 1)
            (assign (secret_lyging_value cs) 1)
            (assign (secret_lyging_value ds) 1)

            (assign (shared_value as) 1)
            (assign (shared_value bs) 1)
            (assign (shared_value cs) 1)
            (assign (shared_value ds) 1)
        )

    
        (:goal (and 
                ;(= (@ep ("+ b [c] + b [b]") (= (secret_value as) 3)) ep.true)
                (= (@ep ("+ b [d] + b [b]") (= (secret_value as) 6)) ep.true)
                
                ;(= (@jp ("b [b] b [a]") (secret_value as)) 1)
                ;(= (@ep ("+ s [b] $ s [c]") (= (secret_value as) 1)) ep.true)
            )
        )

        (:ranges
            (agent_loc integer [1,2])
            (shared_loc integer [0,2])
            (own integer [0,1])
            (sharing integer [0,1])
            (secret_value integer [0,9])
            (secret_lyging_value integer [0,9])
            (shared_value integer [0,9]);??????
        )

        (:rules
            (static (agent_loc a) [] [])
            (static (agent_loc b) [] [])
            (static (agent_loc c) [] [])
            (static (agent_loc d) [] [])
            (static (shared_loc as) [] [])
            (static (shared_loc bs) [] [])
            (static (shared_loc cs) [] [])
            (static (shared_loc ds) [] [])
            (static (own a as) [] [])
            (static (own a bs) [] [])
            (static (own a cs) [] [])
            (static (own a ds) [] [])
            (static (own b as) [] [])
            (static (own b bs) [] [])
            (static (own b cs) [] [])
            (static (own b ds) [] [])
            (static (own c as) [] [])
            (static (own c bs) [] [])
            (static (own c cs) [] [])
            (static (own c ds) [] [])
            (static (own d as) [] [])
            (static (own d bs) [] [])
            (static (own d cs) [] [])
            (static (own d ds) [] [])
            (static (sharing) [] [])
            (1st_poly (secret_value as) [1,2] [,])
            (1st_poly (secret_value bs) [1,2] [,])
            (1st_poly (secret_value cs) [1,2] [,])
            (1st_poly (secret_value ds) [1,2] [,])
            (static (secret_lyging_value as) [] [])
            (static (secret_lyging_value bs) [] [])
            (static (secret_lyging_value cs) [] [])
            (static (secret_lyging_value ds) [] [])
            (static (shared_value as) [] [])
            (static (shared_value bs) [] [])
            (static (shared_value cs) [] [])
            (static (shared_value ds) [] [])
            
        )
    )
    