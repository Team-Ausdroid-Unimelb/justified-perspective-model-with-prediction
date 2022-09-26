;Header and description
(define 
    (domain grapevine)

    ;remove requirements that are not needed
    ; (:requirements :strips)

    ; (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    ; )

    ; un-comment following line if constants are needed
    ;(:constants )

    ; (:predicates ;todo: define predicates here
    ; )


    ; (:functions ;todo: define numeric functions here
    ; )

    ;define actions here
    (:action move_right
        :parameters (?a - agent)
        :precondition (and )
        :effect (and 
            (= (agent_at ?a) (+1))
            (= (shared-a_s) 0)
            (= (shared-b_s) 0)
            (= (shared-c_s) 0)
            (= (shared-d_s) 0)
        )
    )
    
    (:action move_left
        :parameters (?a - agent)
        :precondition (and )
        :effect (and 
            (= (agent_at ?a) (-1))
            (= (shared-a_s) 0)
            (= (shared-b_s) 0)
            (= (shared-c_s) 0)
            (= (shared-d_s) 0)
        )
    )

    (:action sharing
        :parameters (?a - agent, ?s - objects)
        :precondition (and (= (:epistemic b [?a] (= (secret ?s) 't')) 1))
        :effect (and 
            (= (shared-a_s) 0)
            (= (shared-b_s) 0)
            (= (shared-c_s) 0)
            (= (shared-d_s) 0)
            (= (shared ?s) (agent_at ?a))
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