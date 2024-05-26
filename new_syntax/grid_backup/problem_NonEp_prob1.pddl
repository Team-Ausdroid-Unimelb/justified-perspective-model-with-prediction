( define
    (problem non_ep_prob1)
    (:domain grid)

    (:agents
        a b c - agent
    )
    (:objects
        s1 s2 s3 - survivor
        r1 r2 r3 r4 r5 r6 r7 r8 r9 - location
    )


    (:init
        (assign (agent_loc a) 'r1')
        (assign (agent_loc b) 'r4')
        (assign (agent_loc c) 'r9')

        (assign (movable a) 1)
        (assign (movable b) 1)
        (assign (movable c) 1)

        (assign (sharable a) 1)
        (assign (sharable b) 1)
        (assign (sharable c) 1)

        (assign (receivable a) 1)
        (assign (receivable b) 1)
        (assign (receivable c) 1)

        (assign (survivor_loc s1) 'r4')
        (assign (survivor_loc s2) 'r5')
        (assign (survivor_loc s3) 'r8')

        (assign (shared s1) 0)
        (assign (shared s2) 0)
        (assign (shared s3) 0)

        (assign (searched r1) 1)
        (assign (searched r2) 0)
        (assign (searched r3) 0)
        (assign (searched r4) 1)
        (assign (searched r5) 0)
        (assign (searched r6) 0)
        (assign (searched r7) 0)
        (assign (searched r8) 0)
        (assign (searched r9) 1)

        (assign (room_id r1) 'r1')
        (assign (room_id r2) 'r2')
        (assign (room_id r3) 'r3')
        (assign (room_id r4) 'r4')
        (assign (room_id r5) 'r5')
        (assign (room_id r6) 'r6')
        (assign (room_id r7) 'r7')
        (assign (room_id r8) 'r8')
        (assign (room_id r9) 'r9')

; 1 2 3
; 4 5 6
; 7 8 9


        (assign (connected r1 r1) 0)
        (assign (connected r1 r2) 1)
        (assign (connected r1 r3) 0)
        (assign (connected r1 r4) 1)
        (assign (connected r1 r5) 0)
        (assign (connected r1 r6) 0)
        (assign (connected r1 r7) 0)
        (assign (connected r1 r8) 0)
        (assign (connected r1 r9) 0)

        (assign (connected r2 r1) 1)
        (assign (connected r2 r2) 0)
        (assign (connected r2 r3) 1)
        (assign (connected r2 r4) 0)
        (assign (connected r2 r5) 1)
        (assign (connected r2 r6) 0)
        (assign (connected r2 r7) 0)
        (assign (connected r2 r8) 0)
        (assign (connected r2 r9) 0)

        (assign (connected r3 r1) 0)
        (assign (connected r3 r2) 1)
        (assign (connected r3 r3) 0)
        (assign (connected r3 r4) 0)
        (assign (connected r3 r5) 0)
        (assign (connected r3 r6) 1)
        (assign (connected r3 r7) 0)
        (assign (connected r3 r8) 0)
        (assign (connected r3 r9) 0)

        (assign (connected r4 r1) 1)
        (assign (connected r4 r2) 0)
        (assign (connected r4 r3) 0)
        (assign (connected r4 r4) 0)
        (assign (connected r4 r5) 1)
        (assign (connected r4 r6) 0)
        (assign (connected r4 r7) 1)
        (assign (connected r4 r8) 0)
        (assign (connected r4 r9) 0)

        (assign (connected r5 r1) 0)
        (assign (connected r5 r2) 1)
        (assign (connected r5 r3) 0)
        (assign (connected r5 r4) 1)
        (assign (connected r5 r5) 0)
        (assign (connected r5 r6) 1)
        (assign (connected r5 r7) 0)
        (assign (connected r5 r8) 1)
        (assign (connected r5 r9) 0)

        (assign (connected r6 r1) 0)
        (assign (connected r6 r2) 0)
        (assign (connected r6 r3) 1)
        (assign (connected r6 r4) 0)
        (assign (connected r6 r5) 1)
        (assign (connected r6 r6) 0)
        (assign (connected r6 r7) 0)
        (assign (connected r6 r8) 0)
        (assign (connected r6 r9) 1)

        (assign (connected r7 r1) 0)
        (assign (connected r7 r2) 0)
        (assign (connected r7 r3) 0)
        (assign (connected r7 r4) 1)
        (assign (connected r7 r5) 0)
        (assign (connected r7 r6) 0)
        (assign (connected r7 r7) 0)
        (assign (connected r7 r8) 1)
        (assign (connected r7 r9) 0)

        (assign (connected r8 r1) 0)
        (assign (connected r8 r2) 0)
        (assign (connected r8 r3) 0)
        (assign (connected r8 r4) 0)
        (assign (connected r8 r5) 1)
        (assign (connected r8 r6) 0)
        (assign (connected r8 r7) 1)
        (assign (connected r8 r8) 0)
        (assign (connected r8 r9) 1)

        (assign (connected r9 r1) 0)
        (assign (connected r9 r2) 0)
        (assign (connected r9 r3) 0)
        (assign (connected r9 r4) 0)
        (assign (connected r9 r5) 0)
        (assign (connected r9 r6) 1)
        (assign (connected r9 r7) 0)
        (assign (connected r9 r8) 1)
        (assign (connected r9 r9) 0)



        
    )

    (:goal (and 
        (!= (searched r1) 0)
        (!= (searched r2) 0)
        (!= (searched r3) 0)
        (!= (searched r4) 0)
        (!= (searched r5) 0)
        (!= (searched r6) 0)
        (!= (searched r7) 0)
        (!= (searched r8) 0)
        (!= (searched r9) 0)
    ))

    (:ranges
        (agent_loc enumerate ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9'])
        (survivor_loc enumerate ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9'])
        (room_id enumerate ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9'])
        (shared integer [0,1])
        (connected integer [0,1])
        (sharable integer [0,1])
        (movable integer [0,1])
        (receivable integer [0,1])

        ; 0 indicates that room has not been searched neither occupied
        ; 1 indicates that room is occupied
        ; 2 indicates that room has been searched and it is not occupied 
        (searched integer [0,2])
    )

    (:rules
        (static (agent_loc a) [])
        (static (agent_loc b) [])
        (static (agent_loc c) [])

        (static (survivor_loc s1) [])
        (static (survivor_loc s2) [])
        (static (survivor_loc s3) [])

        (static (room_id r1) [])
        (static (room_id r2) [])
        (static (room_id r3) [])
        (static (room_id r4) [])
        (static (room_id r5) [])
        (static (room_id r6) [])
        (static (room_id r7) [])
        (static (room_id r8) [])
        (static (room_id r9) [])

        (static (shared s1) [])
        (static (shared s2) [])
        (static (shared s3) [])

        (static (connected r1 r1) [])
        (static (connected r1 r2) [])
        (static (connected r1 r3) [])
        (static (connected r1 r4) [])
        (static (connected r1 r5) [])
        (static (connected r1 r6) [])
        (static (connected r1 r7) [])
        (static (connected r1 r8) [])
        (static (connected r1 r9) [])

        (static (connected r2 r1) [])
        (static (connected r2 r2) [])
        (static (connected r2 r3) [])
        (static (connected r2 r4) [])
        (static (connected r2 r5) [])
        (static (connected r2 r6) [])
        (static (connected r2 r7) [])
        (static (connected r2 r8) [])
        (static (connected r2 r9) [])

        (static (connected r3 r1) [])
        (static (connected r3 r2) [])
        (static (connected r3 r3) [])
        (static (connected r3 r4) [])
        (static (connected r3 r5) [])
        (static (connected r3 r6) [])
        (static (connected r3 r7) [])
        (static (connected r3 r8) [])
        (static (connected r3 r9) [])

        (static (connected r4 r1) [])
        (static (connected r4 r2) [])
        (static (connected r4 r3) [])
        (static (connected r4 r4) [])
        (static (connected r4 r5) [])
        (static (connected r4 r6) [])
        (static (connected r4 r7) [])
        (static (connected r4 r8) [])
        (static (connected r4 r9) [])

        (static (connected r5 r1) [])
        (static (connected r5 r2) [])
        (static (connected r5 r3) [])
        (static (connected r5 r4) [])
        (static (connected r5 r5) [])
        (static (connected r5 r6) [])
        (static (connected r5 r7) [])
        (static (connected r5 r8) [])
        (static (connected r5 r9) [])

        (static (connected r6 r1) [])
        (static (connected r6 r2) [])
        (static (connected r6 r3) [])
        (static (connected r6 r4) [])
        (static (connected r6 r5) [])
        (static (connected r6 r6) [])
        (static (connected r6 r7) [])
        (static (connected r6 r8) [])
        (static (connected r6 r9) [])

        (static (connected r7 r1) [])
        (static (connected r7 r2) [])
        (static (connected r7 r3) [])
        (static (connected r7 r4) [])
        (static (connected r7 r5) [])
        (static (connected r7 r6) [])
        (static (connected r7 r7) [])
        (static (connected r7 r8) [])
        (static (connected r7 r9) [])

        (static (connected r8 r1) [])
        (static (connected r8 r2) [])
        (static (connected r8 r3) [])
        (static (connected r8 r4) [])
        (static (connected r8 r5) [])
        (static (connected r8 r6) [])
        (static (connected r8 r7) [])
        (static (connected r8 r8) [])
        (static (connected r8 r9) [])

        (static (connected r9 r1) [])
        (static (connected r9 r2) [])
        (static (connected r9 r3) [])
        (static (connected r9 r4) [])
        (static (connected r9 r5) [])
        (static (connected r9 r6) [])
        (static (connected r9 r7) [])
        (static (connected r9 r8) [])
        (static (connected r9 r9) [])

        (static (searched r1) [])
        (static (searched r2) [])
        (static (searched r3) [])
        (static (searched r4) [])
        (static (searched r5) [])
        (static (searched r6) [])
        (static (searched r7) [])
        (static (searched r8) [])
        (static (searched r9) [])

        (static (sharable a) [])
        (static (sharable b) [])
        (static (sharable c) [])

        (static (movable a) [])
        (static (movable b) [])
        (static (movable c) [])



    )
)

