
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
        (peeking [ a , b ,c,d])
        (num [e])
    )

    (:init
        (= (agent_at a) 1)
        (= (agent_at b) 1)
        (= (agent_at c) 1)
        (= (agent_at d) 1)


        (= (shared a) 0)
        (= (shared b) 0)
        (= (shared c) 0)
        (= (shared d) 0)      

        ; constant dummy value to represent knows one's secret_at
        (= (secret a) 't')
        (= (secret b) 't')  
        (= (secret c) 't')  
        (= (secret d) 't')    

        (= (peeking a) 'f')
        (= (peeking b) 'f')
        (= (peeking c) 'f')
        (= (peeking d) 'f')

        (= (num e) 2)      
    )

    (:goal (and
        ; (= (:ontic (= (agent_at a) 2)) 1)
        ; (= (:ontic (= (shared a) 2)) 1)
        ;(= (:epistemic b [b] (= (secret a) 't')) 1)
        (= (:epistemic b [c] (= (secret a) 'f')) 1)
        (= (:epistemic b [a] (= (num e) 4)) 1)
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
        (peeking enumerate ['t','f']) ;
        (num integer [0,20] linear)
        ;(epistemic epistemic ['1','0','2']) true false unknown
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)