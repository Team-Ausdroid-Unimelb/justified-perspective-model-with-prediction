

( define 
    (problem bbl_01) 
    (:domain bbl)

    (:agents
        a b
    )
    (:objects 
        p
    )

    (:variables
        (dir [ a , b ])
        (x [a,b,p])
        (y [a,b,p])
        (g [])
    )

    (:init
        (= (dir a) 'sw')
        (= (dir b) 'sw')
        (= (x a) 3)
        (= (x b) 2)
        (= (x p) 1)
        (= (y a) 3)
        (= (y b) 2)
        (= (y p) 1)
        (= (g) 't')
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        (= (dir b) 's')
        ;todo: put the goal condition here
    ))

    (:domains
        (dir enumerate ['w','nw','n','ne','e','se','s','sw'])
        (x integer [0,4])
        (y integer [0,4])
        (g enumerate ['t','f'])
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)

