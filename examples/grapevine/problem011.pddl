
(define 
    (problem grapevine_01) 
    (:domain grapevine)

    (:agents
        a b c d
    )
        
    (:objects
        p
    )

    (:variables
        (agent_at [a,b,c,d])
        (shared [a,b,c,d])
        (secret [a,b,c,d])
        (secretvalue [a,b,c,d])
        (sharing [a,b,c,d])
        (num [p])
    )

    (:init
        (= (agent_at a) 1)
        (= (agent_at b) 1)
        ;(= (agent_at c) 1)
        (= (agent_at d) 1)
        (= (agent_at c) 2)

        (= (shared a) 0)
        (= (shared b) 0)
        (= (shared c) 0)
        (= (shared d) 0)      


        (= (sharing a) 'f')
        (= (sharing b) 'f')
        (= (sharing c) 'f')
        (= (sharing d) 'f')
        

        ; constant dummy value to represent knows one's secret_at
        (= (secret a) 't')
        (= (secret b) 't')  
        (= (secret c) 't')  
        (= (secret d) 't')  

        (= (secretvalue a) 2) 
        (= (secretvalue b) 2) 
        (= (secretvalue c) 2) 
        (= (secretvalue d) 2)  

    )

    (:goal (and
        ; (= (:ontic (= (agent_at a) 2)) 1)
        ; (= (:ontic (= (shared a) 2)) 1)
        ;(= (:epistemic b [b] (= (secret a) 't')) 1)
        ;(= (:epistemic b [c] (= (secret a) 'f')) 1)
        ;(= (:epistemic b [c] b [b] (= (secretvalue a) 3)) 1)

        ;(= (:epistemic b [b] (= (secretvalue a) 3)) 1)
        ;(= (:epistemic b [a] (= (secretvalue a) 7)) 1)
        ;(= (:epistemic b [c] (= (secretvalue a) 7)) 1)

        ;(= (:epistemic b [b] (= (secret a) 'f')) 1)
        ;(= (:epistemic b [b] (= (secretvalue a) -3)) 1)

        (= (:epistemic b [c] (= (secretvalue a) 4)) 1)
        (= (:epistemic b [b] (= (secret a) 'f')) 1)
        (= (:epistemic b [b] (= (secretvalue a) -7)) 1)
        (= (:epistemic b [c] b [b] (= (secretvalue a) 4)) 1)
        

        ; (= (:epistemic b [d] (= (secret a) 't')) 0)
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
        (secret enumerate ['t','f'])
        (secretvalue integer [0,7] linear)
        (sharing enumerate ['t','f'] static)
        (num integer [0,2])
        ;(epistemic epistemic ['1','0','2']) true false unknown
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)