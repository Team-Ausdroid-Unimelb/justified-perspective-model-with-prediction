
(define 
    (problem grapevine_01) 
    (:domain grapevine)

    (:agents
        a b
    )
        
    (:objects
        p
    )

    (:variables
        (agent_at [a,b])
        (numl [e])
        (nump [f])
    )

    (:init
        (= (agent_at a) 1)
        (= (agent_at b) 1)
        (= (object_at e) 1)
        (= (object_at f) 2)

        (= (numl e) 2)     
        (= (nump f) 1)  
    )

    (:goal (and
        ;(= (:epistemic b [a] (= (nump f) 2)) 1)
        ;(= (:epistemic b [a] (= (numl e) 2)) 1)
        ;(= (:epistemic b [b] (= (numl e) 3)) 1)

        ;(= (:epistemic b [a] b [b] (= (numl e) 4)) 1)

        (= (:epistemic b [a] (= (nump f) 10)) 1)
        (= (:epistemic b [b] (= (nump f) 5)) 1)

    ))

    (:domains
        (agent_at integer [1,2] static)
        (object_at integer [1,2] static)
        (numl integer [0,20] linear) ;2,3,4,5,6
        (nump integer [0,50] 2nd_poly)  ;1,2,5,10,17
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)