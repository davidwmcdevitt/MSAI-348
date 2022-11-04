(define (domain sokorobotto)
  (:requirements :typing)
  (:types shipment order pallette saleitem pallette robot location  - objects
  robot pallette - carrier )
  (:predicates 
  (ships ?x - shipment ?y - order)
  (orders ?x - order ?y - saleitem)
  (unstarted ?x - shipment)
  (started ?x - shipment)
  (packing-location ?x - location)
  (pack ?x - shipment ?y - location)
  (available ?x - location)
  (contains ?x - pallette ?y - saleitem)
  (free ?x - robot)
  (connected ?x ?y - location)
  (at ?x - carrier ?y - location)
  (no-robot ?x - location)
  (no-pallette ?x - location)
  (has-robot ?x - location)
  (has-pallette ?x - location)
  (carrying ?x - robot ?y - pallette)
  (being-carried ?x - pallette ?y - robot)
  (includes ?x - shipment ?y - saleitem)
    )
(:action robot-walk
      :parameters ( ?robot - robot
                    ?start - location
                    ?end - location)
      :precondition (and  (at ?robot ?start)
                          (no-robot ?end)
                          (connected ?start ?end)
                          (free ?robot))
      :effect (and  (no-robot ?start)
                    (at ?robot ?end)
                    (not (at ?robot ?start))
                    (not (no-robot ?end))))
(:action robot-lift
      :parameters ( ?robot - robot
                    ?location - location
                    ?pallette - pallette)
      :precondition (and (at ?robot ?location)
                      (at ?pallette ?location)
                      (free ?robot))
      :effect (and  (not(free ?robot))
                    (carrying ?robot ?pallette)
                    (being-carried ?pallette ?robot)))
(:action robot-walk-with-pallette
      :parameters ( ?robot - robot
                    ?start - location
                    ?end - location
                    ?pallette - pallette)
      :precondition (and  (at ?robot ?start)
                          (no-pallette ?end)
                          (no-robot ?end)
                          (connected ?start ?end)
                          (carrying ?robot ?pallette)
                          (at ?pallette ?start))
      :effect (and  (no-robot ?start)
                    (no-pallette ?start)
                    (has-robot ?end)
                    (has-pallette ?end)
                    (at ?robot ?end)
                    (at ?pallette ?end)
                    (not (at ?robot ?start))
                    (not (at ?pallette ?start))
                    (not (no-robot ?end))
                    (not (no-pallette ?end))
                   ))
(:action build-shipment
      :parameters ( ?location - location
                    ?pallette - pallette
                    ?shipment - shipment
                    ?saleitem - saleitem
                    ?order - order)
      :precondition (and  (contains ?pallette ?saleitem)
                          (orders ?order ?saleitem)
                          (ships ?shipment ?order)
                          (at ?pallette ?location)
                          (has-pallette ?location)
                          (has-robot ?location)
                          (started ?shipment)
                          (pack ?shipment ?location))
      :effect (and  (includes ?shipment ?saleitem)
                    (not (contains ?pallette ?saleitem))
                    (not (unstarted ?shipment))
        
      ))
(:action start-packing
      :parameters ( ?location - location
                    ?shipment - shipment)
        :precondition (and  (available ?location)
                            (packing-location ?location)
        )
        :effect (and  (not(available ?location))
                      (pack ?shipment ?location)
                      (started ?shipment)
                      (not(unstarted ?shipment))
          
        ))
(:action finish-packing
      :parameters ( ?location - location
                    ?shipment - shipment)
        :precondition (and  (packing-location ?location)
                            (pack ?shipment ?location)          
        )
        :effect (and  (not (pack ?shipment ?location))
                      (available ?location)
        ))
(:action robot-put-down
      :parameters   ( ?robot - robot
                      ?location - location
                      ?pallette - pallette)
      :precondition (and  (at ?robot ?location)
                          (carrying ?robot ?pallette)
                          (being-carried ?pallette ?robot)
                          )
      :effect (and  (not(carrying ?robot ?pallette))
                    (not(being-carried ?pallette ?robot))
                    (free ?robot)
                    (has-pallette ?location)
      )))