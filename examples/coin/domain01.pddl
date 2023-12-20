;Header and description

(define 
    (domain coin)

    (:action single_peek
        :parameters (?i - agent)
        :precondition (and 
            (= (:ontic (= (peeking-a) 'f')) 1)
            (= (:ontic (= (peeking-b) 'f')) 1)
        )
        :effect (and 
            (= (peeking ?i) 't')
            
        )
    )

    (:action return
        :parameters (?i - agent)
        :precondition (and 
            ; (= (peeking ?i) 't')
            (= (:ontic (= (peeking ?i) 't')) 1)
        )
        :effect (and 
            (= (peeking ?i) 'f')
        )
    )

)