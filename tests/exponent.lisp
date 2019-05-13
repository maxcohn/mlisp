(defun exp_help (b p a)
    (if (== p 0)
        a
        (exp_help b (- p 1) (* a b))
    )
)

(defun exp (b p)
    (exp_help b p 1)
)

(print (exp 3 4))

