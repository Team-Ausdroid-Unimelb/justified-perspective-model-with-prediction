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
        (secret [a_s,b_s,c_s,d_s])
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

        (= (knows a a_s) 't')
        (= (knows a b_s) 'f')
        (= (knows a c_s) 'f')
        (= (knows a d_s) 'f')
        (= (knows b a_s) 'f')
        (= (knows b b_s) 't')
        (= (knows b c_s) 'f')
        (= (knows b d_s) 'f')
        (= (knows c a_s) 'f')
        (= (knows c b_s) 'f')
        (= (knows c c_s) 't')
        (= (knows c d_s) 'f')
        (= (knows d a_s) 'f')
        (= (knows d b_s) 'f')
        (= (knows d c_s) 'f')
        (= (knows d d_s) 't')

        ; constant dummy value to represent knows one's secret_at
        (= (secret a_s) 't')
        (= (secret b_s) 't')  
        (= (secret c_s) 't')  
        (= (secret d_s) 't')          
    )

    (:goal (and
        ; (= (:ontic (= (agent_at a) 2)) 1)
        ; (= (:ontic (= (shared a) 2)) 1)
        (= (:epistemic k [b] (= (secret a_s) 't')) 1)
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
        (knows enumerate ['t','f'])
        ;(epistemic epistemic ['1','0','2']) true false unknown
    )



    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)