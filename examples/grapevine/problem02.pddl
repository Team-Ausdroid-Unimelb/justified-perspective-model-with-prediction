(define 
    (problem bbl_01) 
    (:domain bbl)

    (:agents
        a b c d
    )
    (:objects 
        a_s b_s c_s d_s
    )

    (:variables
        (agent_at [a,b,c,d])
        (shared [a_s,b_s,c_s,d_s])
        (knows [a,b,c,d] [a_s,b_s,c_s,d_s])
    )

    (:init
        (= (agent_at a) 1)
        (= (agent_at b) 1)
        (= (agent_at c) 1)
        (= (agent_at d) 1)


        (= (shared a_s) 0)
        (= (shared b_s) 0)
        (= (shared c_s) 0)
        (= (shared d_s) 0)        
    )

    (:goal (and
        ; (= (:ontic (= (agent_at a) 2)) 1)
        (= (:ontic (= (shared a) 2)) 1)
        ; (= (:epistemic s [b] (= (v p) 't')) 0)
        ; (= (:epistemic k [b] k [a] (= (v p) 't')) 0)
        ; (= (:epistemic s [b] s [a] (= (v p) 't')) 2)
        ; (= (:epistemic k [b] s [a] (= (v p) 't')) 2)
        ; (= (:epistemic s [a] (= (v p) 't')) 1)
        ; (= (:epistemic b [a] (= (v p) 't')) 1)
        ; (= (:epistemic b [b] (= (v p) 't')) 1)
        ;todo: put the goal condition here
    ))

    (:domains
        (agent_at integer [1,2])
        (shared integer [0,2])
        ;(epistemic epistemic ['1','0','2']) true false unknown
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)