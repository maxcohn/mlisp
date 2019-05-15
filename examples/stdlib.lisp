(defun max (a b)
    (if (> a b) a b)
)

(defun min (a b)
    (if (< a b) a b)
)

(defun and (a b)
    (if (!= a 0)
        (if (!= b 0)
            1
            0
        )
        0
    )
)

(defun or (a b)
    (if (!= a 0)
        1
        (if (!= b 0)
            1
            0
        )
    )
)
