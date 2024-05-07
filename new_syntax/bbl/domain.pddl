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
        ; (room ?r - askable ?b - turnable)
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
    

    ; ((room ?b) "r1")
    ; v_name == "room-a"
    ;     if "room-a" in state.keys():
    ;     else:
    ;         state [(notroom-a-r1)]
    ;         (= (notroom a r2) 1)
    ;         (= (notroom a r3) 0)
    ;         (= (notroom a r4) 1)

    ; (= (notroom a r1) 1)
    ; (= (notroom a r2) 1)
    ; (= (notroom a r3) 0)
    ; (= (notroom a r4) 1)
    ; (:action turn_counter_clockwise
    ;     :parameters (?i - turnable)
    ;     :precondition ()
    ;     :effect (
    ;         (= (dir ?i) 1)
    ;     )
    ; )
 
)