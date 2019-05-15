; classic 0-1 knapsack problem

; k takes arguments:
; m = max weight
; v = list of item values
; w = list of item weight
(defun k (m v w)
    (if (== m 0)
        0
        (if (== (length v) 0)
            0
            (if (> (head w) m)
                (k m (tail w) (tail v))
                (max
                    (+ (k (- m (head w)) (tail w) (tail v)) (head v))
                    (k m (tail w) (tail v))
                )
            )
        )
    )

)

(print (k 50 (list 60 100 120) (list 10 20 30))) ; '220'