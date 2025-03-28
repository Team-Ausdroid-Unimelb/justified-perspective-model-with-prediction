;Header and description
(define 
    (domain number)

    (:types
        agent num
    )

    (:functions
        (peeking ?i - agent)
        (num ?s - num)
    )

    ;define actions here
    (:action single_peek
        :parameters (?i - agent)
        :precondition (and 
            (= (peeking a) 'f')
            (= (peeking b) 'f')
        )
        :effect (and 
            (assign (peeking ?i) 't') 
        )
    )

    (:action return
        :parameters (?i - agent)
        :precondition (and 
            (= (peeking ?i) 't')
        )
        :effect (and 
            (assign (peeking ?i) 'f') 
        )
    )
    
)