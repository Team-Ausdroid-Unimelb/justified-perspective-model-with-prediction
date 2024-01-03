( define 
    (problem num_01) 
    (:domain number)

    (:agents
        a b
    )
    (:objects 
        c
    )

    (:variables
        (peeking [ a , b ])
        (num [c])
        (knows_rule [a , b])
    )

    (:init
        (= (peeking a) 'f')
        (= (peeking b) 'f')
        (= (num c) 2)
        (= (knows_rule a) 'yes') 
        (= (knows_rule b) 'no') 
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and

        (= (:epistemic b [a] (= (num c) 5)) 1)
        (= (:epistemic b [b] b [a] (= (num c) 5)) 1)

        ;todo: put the goal condition here
    ))

    (:domains

        (peeking enumerate ['t','f'])
        (num integer [0,4])

    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
