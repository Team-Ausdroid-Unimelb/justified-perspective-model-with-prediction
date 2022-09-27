;Header and description
(define 
    (domain grapevine)



    ;define actions here
    (:action move_right
        :parameters (?a - agent)
        :precondition (and 
        ; to do
            (= (:ontic (= (agent_at ?a) 1)) 1)
        )
        :effect (and 
            (= (agent_at ?a) (+1))
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
        )
    )
    
    (:action move_left
        :parameters (?a - agent)
        :precondition (and 
            (= (:ontic (= (agent_at ?a) 2)) 1)
        )
        :effect (and 
            (= (agent_at ?a) (-1))
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
        )
    )

    (:action sharing
        :parameters (?a - agent, ?s - agent)
        :precondition (and (= (:epistemic b [?a] (= (secret ?s) 't')) 1))
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (shared ?s) (agent_at ?a))
            (= (secret ?s) 't')  
        )
    )


    (:action sharing_lie
        :parameters (?a - agent, ?s - agent)
        :precondition (and (= (:epistemic b [?a] (= (secret ?s) 't')) 1))
        :effect (and 
            (= (shared-a) 0)
            (= (shared-b) 0)
            (= (shared-c) 0)
            (= (shared-d) 0)
            (= (shared ?s) (agent_at ?a))
            (= (secret ?s) 'f')  
        )
    )
    ; (:action share_bs
    ;     :parameters (?a - agent)
    ;     :precondition (and (= (knows ?a b_s) 1))
    ;     :effect (and 
    ;         (= (shared-a_s) 0)
    ;         (= (shared-b_s) (agent_at ?a))
    ;         (= (shared-c_s) 0)
    ;         (= (shared-d_s) 0)
    ;     )
    ; )

    ; (:action share_cs
    ;     :parameters (?a - agent)
    ;     :precondition (and (= (knows ?a c_s) 1))
    ;     :effect (and 
    ;         (= (shared-a_s) 0)
    ;         (= (shared-b_s) 0)
    ;         (= (shared-c_s) (agent_at ?a))
    ;         (= (shared-d_s) 0)
    ;     )
    ; )

    ; (:action share_as
    ;     :parameters (?a - agent)
    ;     :precondition (and (= (knows ?a a_s) 1))
    ;     :effect (and 
    ;         (= (shared-a_s) (agent_at ?a))
    ;         (= (shared-b_s) 0)
    ;         (= (shared-c_s) 0)
    ;         (= (shared-d_s) 0)
    ;     )
    ; )

    ; (:action share_ds
    ;     :parameters (?a - agent)
    ;     :precondition (and (= (knows ?a d_s) 1))
    ;     :effect (and 
    ;         (= (shared-a_s) 0)
    ;         (= (shared-b_s) 0)
    ;         (= (shared-c_s) 0)
    ;         (= (shared-d_s) (agent_at ?a))
    ;     )
    ; )





)