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
        :precondition (
            (= (dir ?i) (x ?i))
            ; this representation is for return value from justified perspective function
            ; the range of the @jp depends on the variable
            (= (@jp ("b [?i] b [?i]") (v ?i)) 't')
            (!= ((@jp ("b [?i] b [a]") (v ?i))) jp.none)
            ; this representation is for evaluation of en epistemic formula with justified perspective model
            ; the range of the @ep has three possible value, ep.true, ep.unknown and ep.false
            (= (@ep ("+ b [?i] + b [?i]") (= (v ?i) 1)) ep.true)
        )
        :effect (
            ; increase sth by 1
            (increase (dir ?i) 1)
            (assign (x ?i) (@jp ("b [?i] b [a]") (v ?i)))
            (assign (dir ?i) (y ?i))
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