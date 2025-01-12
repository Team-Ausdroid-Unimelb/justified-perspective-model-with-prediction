;Header and description
(define 
    (domain grapevine)

    (:types
        secret agent

    )

    (:functions
        (agent_loc ?a - agent)
        (secret_truth_value ?s - secret);secret_truth_value
        (agent_lyging_value ?a - agent)
        (shared_value ?s - secret)
        (shared_loc ?s - secret)
        (own ?a - agent ?s - secret)
        (sharing)
    )

    ;define actions here
    (:action move_right
        :parameters (?a - agent)
        :precondition (
            (= (agent_loc ?a) 1)
            (= (sharing) 0)
        )
        :effect ( 
            (assign (agent_loc ?a) 2)
        )
    )
    
    (:action move_left
        :parameters (?a - agent)
        :precondition (
             (= (agent_loc ?a) 2)
             (= (sharing) 0)
        )
        :effect (
            (assign (agent_loc ?a) 1)
        )
    )

    (:action quiet
        :parameters (?s - secret)
        :precondition (
            (= (sharing) 1)
            (!= (shared_loc ?s) 0)
        )
        :effect (
            (assign (sharing) 0);constant
            (assign (shared_loc ?s) 0)
            (assign (shared_value ?s) (secret_truth_value ?s));ontic variable
        )
    )
    

    (:action sharing_own_secret
        :parameters (?a - agent, ?s - secret)
        :precondition (
            (= (own ?a ?s) 1)
            (= (sharing) 0)
        )
        :effect (
            (assign (shared_loc ?s) (agent_loc ?a))
            (assign (shared_value ?s) (secret_truth_value ?s))
            (assign (sharing) 1)
            
        )
    )

    (:action lying_own_secret
        :parameters (?a - agent, ?s - secret)
        :precondition (
            (= (own ?a ?s) 1)
            (= (sharing) 0)
        )
        :effect (
            (assign (shared_loc ?s) (agent_loc ?a))
            (assign (shared_value ?s) (agent_lyging_value ?a))
            (assign (sharing) 1)
        )
    )

    (:action sharing_others_secret
        :parameters (?a - agent, ?s - secret)
        :precondition (
            (= (own ?a ?s) 0)
            (= (sharing) 0)
            (!= (@jp ("b [?a]") (shared_value ?s)) jp.none)
        )
        :effect (
            (assign (shared_loc ?s) (agent_loc ?a))
            (assign (shared_value ?s) (@jp ("b [?a]") (shared_value ?s))) 
            (assign (sharing) 1)
        )
    )

    (:action lying_others_secret
        :parameters (?a - agent, ?s - secret)
        :precondition (
            (!= (@jp ("b [?a]") (shared_value ?s)) jp.none)
            (= (sharing) 0)
        )
        :effect (
            (assign (shared_loc ?s) (agent_loc ?a))
            (assign (shared_value ?s) (agent_lyging_value ?a))
            (assign (sharing) 1)
        )
    )
    

)