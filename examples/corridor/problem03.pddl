( define 
    (problem bbl_01) 
    (:domain bbl)

    (:agents
        a b c
    )
    (:objects 
        r1 r2 r3 r4
    )

    (:variables
        (agent_at [a,b,c])
        (secret_at [r1,r2,r3,r4])
        (sensed)
        (shared_at [r1,r2,r3,r4])
    )

    (:init
        (= (agent_at a) 'r1')
        (= (agent_at b) 'r2')
        (= (agent_at c) 'r3')
        (= (secret_at r1) 0)
        (= (secret_at r2) 1)
        (= (secret_at r3) 0)
        (= (secret_at r4) 0)
        (= (sensed) 0)
        (= (shared_at r1) 0)
        (= (shared_at r2) 0)
        (= (shared_at r3) 0)
        (= (shared_at r4) 0)
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ; (= (:ontic (= (agent_at a) 2)) 1)
        ; (= (:ontic (= (shared s) 2)) 1)
        (= (:epistemic b [b] (= (shared s) 2)) 1)
        ; (= (:epistemic k [b] k [a] (= (v p) 't')) 0)
        ; (= (:epistemic s [b] s [a] (= (v p) 't')) 2)
        ; (= (:epistemic k [b] s [a] (= (v p) 't')) 2)
        ; (= (:epistemic s [a] (= (v p) 't')) 1)
        ; (= (:epistemic b [a] (= (v p) 't')) 1)
        ; (= (:epistemic b [b] (= (v p) 't')) 1)
        ;todo: put the goal condition here
    ))

    (:domains
        (agent_at enumerate ['r1','r2','r3','r4'])
        (secret_at integer [1,4])
        (sensed enumerate ['t','f'])
        ;(epistemic epistemic ['1','0','2']) true false unknown
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)