;Header and description
(define 
    (domain grapevine)



    ;define actions here
    (:action move_right
        :parameters (?a - agent)
        :precondition (and 
            (= (:ontic (= (agent_at ?a) 1)) 1)
            (= (:ontic (= (sharing-a) 'f')) 1)
            (= (:ontic (= (sharing-b) 'f')) 1)
            (= (:ontic (= (sharing-c) 'f')) 1)
            (= (:ontic (= (sharing-d) 'f')) 1)

            )
        :effect (and 
            (= (agent_at ?a) (+1))
        )
    )
    
    (:action move_left
        :parameters (?a - agent)
        :precondition (and 
            (= (:ontic (= (agent_at ?a) 2)) 1)
            (= (:ontic (= (sharing-a) 'f')) 1)
            (= (:ontic (= (sharing-b) 'f')) 1)
            (= (:ontic (= (sharing-c) 'f')) 1)
            (= (:ontic (= (sharing-d) 'f')) 1)

        )
        :effect (and 
            (= (agent_at ?a) (-1))
            
        )
    )
    (:action sharing_truth
        :parameters (?a - agent, ?s - agent)
        :precondition (and 
            (= (:epistemic b [?a] (= (secret ?s) 't')) 1)
            ;(not (= ?a ?s))
            )
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?s) (agent_at ?a))
            (= (secret ?s) 't')
            (= (sharing ?s) 't')
            
        )
    )

    (:action sharing_false
        :parameters (?a - agent, ?s - agent)
        :precondition (and (= (:epistemic b [?a] (= (secret ?s) 'f')) 1))
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?s) (agent_at ?a))
            (= (secret ?s) 'f')
            (= (sharing ?s) 't')
            ; (= (sharing ?a) 1)
            
        )
    )
    (:action sharing
        :parameters (?a - agent)
        :precondition (and 
            (= (:ontic (= (sharing-a) 'f')) 1)
            (= (:ontic (= (sharing-b) 'f')) 1)
            (= (:ontic (= (sharing-c) 'f')) 1)
            (= (:ontic (= (sharing-d) 'f')) 1)

        )
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?a) (agent_at ?a))
            (= (secret ?a) 't')
            ; (= (sharing ?a) 1)
            (= (sharing ?a) 't')
        )
    )

    (:action lying
        :parameters (?a - agent)
        :precondition (and 
            (= (:ontic (= (sharing-a) 'f')) 1)
            (= (:ontic (= (sharing-b) 'f')) 1)
            (= (:ontic (= (sharing-c) 'f')) 1)
            (= (:ontic (= (sharing-d) 'f')) 1)

        )
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
            (= (shared ?a) (agent_at ?a))
            (= (secret ?a) 'f')
            (= (sharing ?a) 't')
            ; (= (sharing ?a) 1)
        )
    
    )
    (:action return
        :parameters (?a - agent)
        :precondition (and 
            (= (:ontic (= (sharing ?a) 't')) 1)
        )
        :effect (and 
            (= (sharing ?a) 'f')
            (= (shared ?a) 0)
            
        )
    )
    
    
)