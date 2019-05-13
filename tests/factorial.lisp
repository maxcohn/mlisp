(defun fact (n)
    (if (<= n 1)
        n
        (* n (fact (- n 1)))
    )
)


(defun fact (n) (if (<= n 1) n (* n (fact (- n 1)))))