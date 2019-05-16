;
;
;
;
(defun mod (a b)
    (- a (* b (/ a b)))
)

(defun ismult (n)
    (if (== (mod n 3) 0) ; if multiple of 3
        1
        (if (== (mod n 5) 0) 1 0)
    )
)

; brute force solution
; lets test how the interpreter handles this

; UPDATE: blows the recursion stack at 1000, but 100 works
(defun rec (n)
    (if n ; if n is positive
        (+ (if (ismult n) n 0) (rec (- n 1)))
        0 ; base case
    )
)

(print (rec 100))