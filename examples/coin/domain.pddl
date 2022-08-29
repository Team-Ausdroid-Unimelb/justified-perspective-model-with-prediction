;Header and description

(define 
    (domain coin)

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
    (:action peek
        :parameters (?i - coin)
        :precondition (and (= (peeking ?i) 'f'))
        :effect (and 
            (= (peeking ?i) 't')
        )
    )

    (:action back
        :parameters (?i - coin)
        :precondition (and (= (peeking ?i) 't'))
        :effect (and 
            (= (peeking ?i) 'f')
        )
    )

    (:action turn_coin
        :parameters (?i - coin)
        :precondition (and )
        :effect (and 
            (= (face ?i) ((face ?i) - 1))
        )
    )
 
)