;Header and description
(define 
    (domain grapevine)



    ;define actions here
    (:action move_right
        :parameters (?a - agent)
        :precondition (and 
            (:ontic (= (agent_at ?a) 1))
        )
        :effect (and 
            (= (agent_at ?a) (+1))
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (secret-a) 't')
            (= (secret-b) 't')
            (= (secret-c) 't')
            (= (secret-d) 't')
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
        )
    )
    
    (:action move_left
        :parameters (?a - agent)
        :precondition (and 
             (:ontic (= (agent_at ?a) 2))
        )
        :effect (and 
            (= (agent_at ?a) (-1))
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (secret-a) 't')
            (= (secret-b) 't')
            (= (secret-c) 't')
            (= (secret-d) 't')
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
        )
    )

    (:action sharing_truth
        :parameters (?a - agent, ?s - agent)
        :precondition (and 
            (:epistemic + b [?a] (= (secret ?s) 't'))
        )
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (secret-a) 't')
            (= (secret-b) 't')
            (= (secret-c) 't')
            (= (secret-d) 't')
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?s) (agent_at ?a))
            (= (secret ?s) 't')
            ; (= (sharing ?a) 1)
            
        )
    )

    (:action sharing_false
        :parameters (?a - agent, ?s - agent)
        :precondition (and 
            (:epistemic + b [?a] (= (secret ?s) 'f'))
        )
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (secret-a) 't')
            (= (secret-b) 't')
            (= (secret-c) 't')
            (= (secret-d) 't')
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?s) (agent_at ?a))
            (= (secret ?s) 'f')
            ; (= (sharing ?a) 1)
            
        )
    )

    (:action sharing
        :parameters (?a - agent)
        :precondition (and )
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (secret-a) 't')
            (= (secret-b) 't')
            (= (secret-c) 't')
            (= (secret-d) 't')
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?a) (agent_at ?a))
            (= (secret ?a) 't')
            ; (= (sharing ?a) 1)
        )
    )

    (:action lying
        :parameters (?a - agent)
        :precondition (and )
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (secret-a) 't')
            (= (secret-b) 't')
            (= (secret-c) 't')
            (= (secret-d) 't')
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?a) (agent_at ?a))
            (= (secret ?a) 'f')
            ; (= (sharing ?a) 1)
        )
    )

)