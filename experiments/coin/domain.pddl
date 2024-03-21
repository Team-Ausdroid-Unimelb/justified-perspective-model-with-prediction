;Header and description

(define 
    (domain coin)

    ;define actions here
    (:action peek
        :parameters (?i - agent)
        :precondition (and 
            ;(= (peeking ?i) 'f')
            (:ontic (= (peeking ?i) 'f'))
        )
        :effect (and 
            (= (peeking ?i) 't')
            
        )
    )

    ; (:action single_peek
    ;     :parameters (?i - agent)
    ;     :precondition (and 
    ;         (= (:ontic (= (peeking-a) 'f')) 1)
    ;         (= (:ontic (= (peeking-b) 'f')) 1)
    ;     )
    ;     :effect (and 
    ;         (= (peeking ?i) 't')
            
    ;     )
    ; )

    (:action return
        :parameters (?i - agent)
        :precondition (and 
            ; (= (peeking ?i) 't')
            (:ontic (= (peeking ?i) 't'))
        )
        :effect (and 
            (= (peeking ?i) 'f')
        )
    )

    (:action turn_coin
        :parameters (?i - object)
        :precondition (and )
        :effect (and 
            (= (face ?i) (-1)))
        )
    )
 
)