;Header and description
(define 
    (domain grapevine)



    ;define actions here
    (:action move_right
        :parameters (?a - agent)
        :precondition (and (= (:ontic (= (agent_at ?a) 1)) 1))
        :effect (and 
            (= (agent_at ?a) (+1))
            ;(= (shared-a) 0)
            ;(= (shared-b) 0)
            ;(= (shared-c) 0)
            ;(= (shared-d) 0)
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
        )
    )
    
    (:action move_left
        :parameters (?a - agent)
        :precondition (and 
            (= (:ontic (= (agent_at ?a) 2)) 1)
        )
        :effect (and 
            (= (agent_at ?a) (-1))
            ;(= (shared-a) 0)
            ;(= (shared-b) 0)
            ;(= (shared-c) 0)
            ;(= (shared-d) 0)
            ; (= (sharing-a) 0)
            ; (= (sharing-b) 0)
            ; (= (sharing-c) 0)
            ; (= (sharing-d) 0)
        )
    )

    
)