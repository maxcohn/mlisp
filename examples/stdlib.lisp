; Max of two values
(defun max (a b)
    (if (> a b) a b)
)

; Min of two values
(defun min (a b)
    (if (< a b) a b)
)

; Logical NOT
(defun not (a)
    (if a 0 1)
)

; Logical AND
(defun and (a b)
    (if a
        (if b
            1
            0
        )
        0
    )
)

; Logical OR
(defun or (a b)
    (if a
        1
        (if b
            1
            0
        )
    )
)

; Logical XOR
(defun xor (a b)
    (if a
        (if (not b)
            1
            0
        )
        (if b
            1
            0
        )
    )
)

; Modular division
(defun mod (a b)
    (- a (* b (/ a b)))
)