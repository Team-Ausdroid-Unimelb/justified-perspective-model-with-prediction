( define 
    (problem bbl_01) 
    (:domain bbl)

    (:agents
        a b c
    )
    (:objects 
        s
    )

    (:variables
        (agent_at [a,b,c])
        (secret_at [s])
        (sensed [s])
    )

    (:init
        (= (agent_at a) 1)
        (= (agent_at b) 2)
        (= (agent_at c) 3)
        (= (secret_at s) 2)
        (= (sensed s) 'f')
        (= (shared s) 0)
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ; (= (:ontic (= (agent_at a) 2)) 1)
        (= (:ontic (= (shared s) 2)) 1)
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
        (agent_at integer [1,4])
        (secret_at integer [1,4])
        (sensed enumerate ['t','f'])
        (shared integer [0,4])
        ;(epistemic epistemic ['1','0','2']) true false unknown
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)