(define 
    (domain bbl)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        locatable
        turnable askable actable - locatable
    )



    (:functions 
        (dir ?a - turnable)
        (x ?a - locatable)
        (y ?a - locatable)
        (v ?a - askable)
        (actable ?a - turnable)
    )

    ;define actions here
    (:action turn_clockwise
        :parameters (?i - turnable)
        :precondition (
            (= (actable ?i) 1)
        )
        :effect (
            ; increase sth by 1
            (increase (dir ?i) 1)
        )
    )

    (:action turn_anti_clockwise
        :parameters (?i - turnable)
        :precondition (
            (= (actable ?i) 1)
        )
        :effect (
            ; increase sth by 1
            (decrease (dir ?i) 1)
        )
    )
 
)