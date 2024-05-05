;Header and description

(define 
    (domain bbl)

    ;remove requirements that are not needed
    ; (:requirements :strips)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        locatable
        turnable askable - locatable
    )

    ; un-comment following line if constants are needed
    ;(:constants )

    ; (:predicates ;todo: define predicates here
    ; )


    (:functions ;todo: define numeric functions here
        ; this is V from model
        (dir ?a - turnable)
        (x ?a - locatable)
        (y ?a - locatable)
        (v ?a - askable)
    )

    ;define actions here
    (:action turn_clockwise
        :parameters (?i - turnable)
        :precondition ()
        :effect (
            ; increase sth by 1
            ; (increase (dir ?i) 1)
            (when (!= ((@jp ("b [?i] b [a]") (v?i))) None) (assign (x ?i) (@jp ("b [b] b [a]") (v?i))))
            ; (assign (dir ?i) (v ?i))
        )
    )
    
    ; (:action turn_counter_clockwise
    ;     :parameters (?i - turnable)
    ;     :precondition ()
    ;     :effect (
    ;         (= (dir ?i) 1)
    ;     )
    ; )
 
)