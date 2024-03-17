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
       
    )

    (:init
        (= (peeking a) 'f')
        (= (peeking b) 'f')
        (= (num c) 2)
 
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal (and
        ;a,b get different blief
        ;a know is 5
        ;b think is 3
        ;b think a see 3

        (= (:epistemic b [a] (= (num c) 7)) 1)
        (= (:epistemic b [b] (= (num c) 3)) 1)
        (= (:epistemic b [b] b [a] (= (num c) 3)) 1)
        (= (:epistemic b [a] b [b] (= (num c) 3)) 1)
        ;(= (:ontic (= (peeking b) 'f')) 1)
        
    ))

    (:domains
        (peeking enumerate ['t','f'] static) ;
        (num integer [0,8] linear)
    ;static, linear, sin, 2nd_poly

    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
