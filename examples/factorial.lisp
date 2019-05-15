(defun fact (n)
    (if (<= n 1)
        n
        (* n (fact (- n 1)))
    )
)

(print "fact of 6")
(print (fact 6))
; (defun fact (n) (if (<= n 1) n (* n (fact (- n 1)))))