

( define 
    (problem bbl_05) 
    (:domain bbl)

    (:agents
        a 
    )
    (:objects 
        p 
    )

    (:variables
        (dir [a])
        (x [a,b,p])
        (y [a,b,p])
        (v [p])
        (tur [b])

    )

    (:init
        (= (dir a) 'n')
        (= (tur b) 'ne')
        (= (x a) 2)
        (= (y a) 1)
        (= (x p) 1)
        (= (y p) 0)
        (= (x b) 1)
        (= (y b) 2)
        (= (v p) 't')

        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;(= (:ontic (= (tur b) 's')) 1)
        ; (= (:epistemic b [b] (= (v p) 't')) 1)
        ; (= (:epistemic k [b] k [a] (= (v p) 't')) 0)
        ;(= (:epistemic b [b] b [a] (= (v p) 't')) 1)
        (= (:epistemic b [a] (= (tur b) 's')) 1)
        (= (:epistemic b [a] (= (v p) 't')) 1)
        ; (= (:epistemic k [b] s [a] (= (v p) 't')) 2)
        ; (= (:epistemic s [a] (= (v p) 't')) 1)
        ; (= (:epistemic b [a] (= (v p) 't')) 1)
        ; (= (:epistemic b [b] (= (v p) 't')) 1)
        ;todo: put the goal condition here
    ))

    (:domains
        (dir enumerate ['w','nw','n','ne','e','se','s','sw'] static)
        (tur enumerate ['w','nw','n','ne','e','se','s','sw'] turning)
        (x integer [0,4] static)
        (y integer [0,4] static)
        (v enumerate ['t','f'] static)
        ;(epistemic epistemic ['1','0','2']) true false unknown
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)

