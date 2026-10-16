; example: encoding int, horizon T = 11
; benchmark generated from python API
(set-info :status unknown)
(declare-fun x_0_0 () Int)
(declare-fun y_0_0 () Int)
(declare-fun x_1_0 () Int)
(declare-fun y_1_0 () Int)
(declare-fun x_2_0 () Int)
(declare-fun y_2_0 () Int)
(declare-fun x_0_1 () Int)
(declare-fun y_0_1 () Int)
(declare-fun x_1_1 () Int)
(declare-fun y_1_1 () Int)
(declare-fun x_2_1 () Int)
(declare-fun y_2_1 () Int)
(declare-fun x_0_2 () Int)
(declare-fun y_0_2 () Int)
(declare-fun x_1_2 () Int)
(declare-fun y_1_2 () Int)
(declare-fun x_2_2 () Int)
(declare-fun y_2_2 () Int)
(declare-fun x_0_3 () Int)
(declare-fun y_0_3 () Int)
(declare-fun x_1_3 () Int)
(declare-fun y_1_3 () Int)
(declare-fun x_2_3 () Int)
(declare-fun y_2_3 () Int)
(declare-fun x_0_4 () Int)
(declare-fun y_0_4 () Int)
(declare-fun x_1_4 () Int)
(declare-fun y_1_4 () Int)
(declare-fun x_2_4 () Int)
(declare-fun y_2_4 () Int)
(declare-fun x_0_5 () Int)
(declare-fun y_0_5 () Int)
(declare-fun x_1_5 () Int)
(declare-fun y_1_5 () Int)
(declare-fun x_2_5 () Int)
(declare-fun y_2_5 () Int)
(declare-fun x_0_6 () Int)
(declare-fun y_0_6 () Int)
(declare-fun x_1_6 () Int)
(declare-fun y_1_6 () Int)
(declare-fun x_2_6 () Int)
(declare-fun y_2_6 () Int)
(declare-fun x_0_7 () Int)
(declare-fun y_0_7 () Int)
(declare-fun x_1_7 () Int)
(declare-fun y_1_7 () Int)
(declare-fun x_2_7 () Int)
(declare-fun y_2_7 () Int)
(declare-fun x_0_8 () Int)
(declare-fun y_0_8 () Int)
(declare-fun x_1_8 () Int)
(declare-fun y_1_8 () Int)
(declare-fun x_2_8 () Int)
(declare-fun y_2_8 () Int)
(declare-fun x_0_9 () Int)
(declare-fun y_0_9 () Int)
(declare-fun x_1_9 () Int)
(declare-fun y_1_9 () Int)
(declare-fun x_2_9 () Int)
(declare-fun y_2_9 () Int)
(declare-fun x_0_10 () Int)
(declare-fun y_0_10 () Int)
(declare-fun x_1_10 () Int)
(declare-fun y_1_10 () Int)
(declare-fun x_2_10 () Int)
(declare-fun y_2_10 () Int)
(declare-fun x_0_11 () Int)
(declare-fun y_0_11 () Int)
(declare-fun x_1_11 () Int)
(declare-fun y_1_11 () Int)
(declare-fun x_2_11 () Int)
(declare-fun y_2_11 () Int)
(assert
 (= x_0_0 1))
(assert
 (= y_0_0 1))
(assert
 (>= x_0_0 0))
(assert
 (< x_0_0 8))
(assert
 (>= y_0_0 0))
(assert
 (< y_0_0 8))
(assert
 (not (and (= x_0_0 3) (= y_0_0 2))))
(assert
 (not (and (= x_0_0 3) (= y_0_0 3))))
(assert
 (not (and (= x_0_0 3) (= y_0_0 4))))
(assert
 (not (and (= x_0_0 5) (= y_0_0 5))))
(assert
 (= x_1_0 7))
(assert
 (= y_1_0 1))
(assert
 (>= x_1_0 0))
(assert
 (< x_1_0 8))
(assert
 (>= y_1_0 0))
(assert
 (< y_1_0 8))
(assert
 (not (and (= x_1_0 3) (= y_1_0 2))))
(assert
 (not (and (= x_1_0 3) (= y_1_0 3))))
(assert
 (not (and (= x_1_0 3) (= y_1_0 4))))
(assert
 (not (and (= x_1_0 5) (= y_1_0 5))))
(assert
 (= x_2_0 1))
(assert
 (= y_2_0 7))
(assert
 (>= x_2_0 0))
(assert
 (< x_2_0 8))
(assert
 (>= y_2_0 0))
(assert
 (< y_2_0 8))
(assert
 (not (and (= x_2_0 3) (= y_2_0 2))))
(assert
 (not (and (= x_2_0 3) (= y_2_0 3))))
(assert
 (not (and (= x_2_0 3) (= y_2_0 4))))
(assert
 (not (and (= x_2_0 5) (= y_2_0 5))))
(assert
 (or (and (distinct x_0_0 x_1_0) true) (and (distinct y_0_0 y_1_0) true)))
(assert
 (or (and (distinct x_0_0 x_2_0) true) (and (distinct y_0_0 y_2_0) true)))
(assert
 (or (and (distinct x_1_0 x_2_0) true) (and (distinct y_1_0 y_2_0) true)))
(assert
 (>= x_0_1 0))
(assert
 (< x_0_1 8))
(assert
 (>= y_0_1 0))
(assert
 (< y_0_1 8))
(assert
 (not (and (= x_0_1 3) (= y_0_1 2))))
(assert
 (not (and (= x_0_1 3) (= y_0_1 3))))
(assert
 (not (and (= x_0_1 3) (= y_0_1 4))))
(assert
 (not (and (= x_0_1 5) (= y_0_1 5))))
(assert
 (or (and (= x_0_1 (+ x_0_0 0)) (= y_0_1 (+ y_0_0 0))) (and (= x_0_1 (+ x_0_0 1)) (= y_0_1 (+ y_0_0 0))) (and (= x_0_1 (+ x_0_0 (- 1))) (= y_0_1 (+ y_0_0 0))) (and (= x_0_1 (+ x_0_0 0)) (= y_0_1 (+ y_0_0 1))) (and (= x_0_1 (+ x_0_0 0)) (= y_0_1 (+ y_0_0 (- 1))))))
(assert
 (>= x_1_1 0))
(assert
 (< x_1_1 8))
(assert
 (>= y_1_1 0))
(assert
 (< y_1_1 8))
(assert
 (not (and (= x_1_1 3) (= y_1_1 2))))
(assert
 (not (and (= x_1_1 3) (= y_1_1 3))))
(assert
 (not (and (= x_1_1 3) (= y_1_1 4))))
(assert
 (not (and (= x_1_1 5) (= y_1_1 5))))
(assert
 (or (and (= x_1_1 (+ x_1_0 0)) (= y_1_1 (+ y_1_0 0))) (and (= x_1_1 (+ x_1_0 1)) (= y_1_1 (+ y_1_0 0))) (and (= x_1_1 (+ x_1_0 (- 1))) (= y_1_1 (+ y_1_0 0))) (and (= x_1_1 (+ x_1_0 0)) (= y_1_1 (+ y_1_0 1))) (and (= x_1_1 (+ x_1_0 0)) (= y_1_1 (+ y_1_0 (- 1))))))
(assert
 (>= x_2_1 0))
(assert
 (< x_2_1 8))
(assert
 (>= y_2_1 0))
(assert
 (< y_2_1 8))
(assert
 (not (and (= x_2_1 3) (= y_2_1 2))))
(assert
 (not (and (= x_2_1 3) (= y_2_1 3))))
(assert
 (not (and (= x_2_1 3) (= y_2_1 4))))
(assert
 (not (and (= x_2_1 5) (= y_2_1 5))))
(assert
 (or (and (= x_2_1 (+ x_2_0 0)) (= y_2_1 (+ y_2_0 0))) (and (= x_2_1 (+ x_2_0 1)) (= y_2_1 (+ y_2_0 0))) (and (= x_2_1 (+ x_2_0 (- 1))) (= y_2_1 (+ y_2_0 0))) (and (= x_2_1 (+ x_2_0 0)) (= y_2_1 (+ y_2_0 1))) (and (= x_2_1 (+ x_2_0 0)) (= y_2_1 (+ y_2_0 (- 1))))))
(assert
 (or (and (distinct x_0_1 x_1_1) true) (and (distinct y_0_1 y_1_1) true)))
(assert
 (let (($x343 (and (= x_0_0 x_1_1) (= y_0_0 y_1_1) (= x_1_0 x_0_1) (= y_1_0 y_0_1))))
 (not $x343)))
(assert
 (or (and (distinct x_0_1 x_2_1) true) (and (distinct y_0_1 y_2_1) true)))
(assert
 (let (($x357 (and (= x_0_0 x_2_1) (= y_0_0 y_2_1) (= x_2_0 x_0_1) (= y_2_0 y_0_1))))
 (not $x357)))
(assert
 (or (and (distinct x_1_1 x_2_1) true) (and (distinct y_1_1 y_2_1) true)))
(assert
 (let (($x371 (and (= x_1_0 x_2_1) (= y_1_0 y_2_1) (= x_2_0 x_1_1) (= y_2_0 y_1_1))))
 (not $x371)))
(assert
 (>= x_0_2 0))
(assert
 (< x_0_2 8))
(assert
 (>= y_0_2 0))
(assert
 (< y_0_2 8))
(assert
 (not (and (= x_0_2 3) (= y_0_2 2))))
(assert
 (not (and (= x_0_2 3) (= y_0_2 3))))
(assert
 (not (and (= x_0_2 3) (= y_0_2 4))))
(assert
 (not (and (= x_0_2 5) (= y_0_2 5))))
(assert
 (or (and (= x_0_2 (+ x_0_1 0)) (= y_0_2 (+ y_0_1 0))) (and (= x_0_2 (+ x_0_1 1)) (= y_0_2 (+ y_0_1 0))) (and (= x_0_2 (+ x_0_1 (- 1))) (= y_0_2 (+ y_0_1 0))) (and (= x_0_2 (+ x_0_1 0)) (= y_0_2 (+ y_0_1 1))) (and (= x_0_2 (+ x_0_1 0)) (= y_0_2 (+ y_0_1 (- 1))))))
(assert
 (>= x_1_2 0))
(assert
 (< x_1_2 8))
(assert
 (>= y_1_2 0))
(assert
 (< y_1_2 8))
(assert
 (not (and (= x_1_2 3) (= y_1_2 2))))
(assert
 (not (and (= x_1_2 3) (= y_1_2 3))))
(assert
 (not (and (= x_1_2 3) (= y_1_2 4))))
(assert
 (not (and (= x_1_2 5) (= y_1_2 5))))
(assert
 (or (and (= x_1_2 (+ x_1_1 0)) (= y_1_2 (+ y_1_1 0))) (and (= x_1_2 (+ x_1_1 1)) (= y_1_2 (+ y_1_1 0))) (and (= x_1_2 (+ x_1_1 (- 1))) (= y_1_2 (+ y_1_1 0))) (and (= x_1_2 (+ x_1_1 0)) (= y_1_2 (+ y_1_1 1))) (and (= x_1_2 (+ x_1_1 0)) (= y_1_2 (+ y_1_1 (- 1))))))
(assert
 (>= x_2_2 0))
(assert
 (< x_2_2 8))
(assert
 (>= y_2_2 0))
(assert
 (< y_2_2 8))
(assert
 (not (and (= x_2_2 3) (= y_2_2 2))))
(assert
 (not (and (= x_2_2 3) (= y_2_2 3))))
(assert
 (not (and (= x_2_2 3) (= y_2_2 4))))
(assert
 (not (and (= x_2_2 5) (= y_2_2 5))))
(assert
 (or (and (= x_2_2 (+ x_2_1 0)) (= y_2_2 (+ y_2_1 0))) (and (= x_2_2 (+ x_2_1 1)) (= y_2_2 (+ y_2_1 0))) (and (= x_2_2 (+ x_2_1 (- 1))) (= y_2_2 (+ y_2_1 0))) (and (= x_2_2 (+ x_2_1 0)) (= y_2_2 (+ y_2_1 1))) (and (= x_2_2 (+ x_2_1 0)) (= y_2_2 (+ y_2_1 (- 1))))))
(assert
 (or (and (distinct x_0_2 x_1_2) true) (and (distinct y_0_2 y_1_2) true)))
(assert
 (let (($x570 (= y_1_1 y_0_2)))
 (let (($x569 (= x_1_1 x_0_2)))
 (let (($x568 (= y_0_1 y_1_2)))
 (let (($x567 (= x_0_1 x_1_2)))
 (not (and $x567 $x568 $x569 $x570)))))))
(assert
 (or (and (distinct x_0_2 x_2_2) true) (and (distinct y_0_2 y_2_2) true)))
(assert
 (let (($x584 (= y_2_1 y_0_2)))
 (let (($x583 (= x_2_1 x_0_2)))
 (let (($x582 (= y_0_1 y_2_2)))
 (let (($x581 (= x_0_1 x_2_2)))
 (not (and $x581 $x582 $x583 $x584)))))))
(assert
 (or (and (distinct x_1_2 x_2_2) true) (and (distinct y_1_2 y_2_2) true)))
(assert
 (let (($x598 (= y_2_1 y_1_2)))
 (let (($x597 (= x_2_1 x_1_2)))
 (let (($x596 (= y_1_1 y_2_2)))
 (let (($x595 (= x_1_1 x_2_2)))
 (not (and $x595 $x596 $x597 $x598)))))))
(assert
 (>= x_0_3 0))
(assert
 (< x_0_3 8))
(assert
 (>= y_0_3 0))
(assert
 (< y_0_3 8))
(assert
 (not (and (= x_0_3 3) (= y_0_3 2))))
(assert
 (not (and (= x_0_3 3) (= y_0_3 3))))
(assert
 (not (and (= x_0_3 3) (= y_0_3 4))))
(assert
 (not (and (= x_0_3 5) (= y_0_3 5))))
(assert
 (or (and (= x_0_3 (+ x_0_2 0)) (= y_0_3 (+ y_0_2 0))) (and (= x_0_3 (+ x_0_2 1)) (= y_0_3 (+ y_0_2 0))) (and (= x_0_3 (+ x_0_2 (- 1))) (= y_0_3 (+ y_0_2 0))) (and (= x_0_3 (+ x_0_2 0)) (= y_0_3 (+ y_0_2 1))) (and (= x_0_3 (+ x_0_2 0)) (= y_0_3 (+ y_0_2 (- 1))))))
(assert
 (>= x_1_3 0))
(assert
 (< x_1_3 8))
(assert
 (>= y_1_3 0))
(assert
 (< y_1_3 8))
(assert
 (not (and (= x_1_3 3) (= y_1_3 2))))
(assert
 (not (and (= x_1_3 3) (= y_1_3 3))))
(assert
 (not (and (= x_1_3 3) (= y_1_3 4))))
(assert
 (not (and (= x_1_3 5) (= y_1_3 5))))
(assert
 (or (and (= x_1_3 (+ x_1_2 0)) (= y_1_3 (+ y_1_2 0))) (and (= x_1_3 (+ x_1_2 1)) (= y_1_3 (+ y_1_2 0))) (and (= x_1_3 (+ x_1_2 (- 1))) (= y_1_3 (+ y_1_2 0))) (and (= x_1_3 (+ x_1_2 0)) (= y_1_3 (+ y_1_2 1))) (and (= x_1_3 (+ x_1_2 0)) (= y_1_3 (+ y_1_2 (- 1))))))
(assert
 (>= x_2_3 0))
(assert
 (< x_2_3 8))
(assert
 (>= y_2_3 0))
(assert
 (< y_2_3 8))
(assert
 (not (and (= x_2_3 3) (= y_2_3 2))))
(assert
 (not (and (= x_2_3 3) (= y_2_3 3))))
(assert
 (not (and (= x_2_3 3) (= y_2_3 4))))
(assert
 (not (and (= x_2_3 5) (= y_2_3 5))))
(assert
 (or (and (= x_2_3 (+ x_2_2 0)) (= y_2_3 (+ y_2_2 0))) (and (= x_2_3 (+ x_2_2 1)) (= y_2_3 (+ y_2_2 0))) (and (= x_2_3 (+ x_2_2 (- 1))) (= y_2_3 (+ y_2_2 0))) (and (= x_2_3 (+ x_2_2 0)) (= y_2_3 (+ y_2_2 1))) (and (= x_2_3 (+ x_2_2 0)) (= y_2_3 (+ y_2_2 (- 1))))))
(assert
 (or (and (distinct x_0_3 x_1_3) true) (and (distinct y_0_3 y_1_3) true)))
(assert
 (let (($x798 (= y_1_2 y_0_3)))
 (let (($x797 (= x_1_2 x_0_3)))
 (let (($x796 (= y_0_2 y_1_3)))
 (let (($x795 (= x_0_2 x_1_3)))
 (not (and $x795 $x796 $x797 $x798)))))))
(assert
 (or (and (distinct x_0_3 x_2_3) true) (and (distinct y_0_3 y_2_3) true)))
(assert
 (let (($x812 (= y_2_2 y_0_3)))
 (let (($x811 (= x_2_2 x_0_3)))
 (let (($x810 (= y_0_2 y_2_3)))
 (let (($x809 (= x_0_2 x_2_3)))
 (not (and $x809 $x810 $x811 $x812)))))))
(assert
 (or (and (distinct x_1_3 x_2_3) true) (and (distinct y_1_3 y_2_3) true)))
(assert
 (let (($x826 (= y_2_2 y_1_3)))
 (let (($x825 (= x_2_2 x_1_3)))
 (let (($x824 (= y_1_2 y_2_3)))
 (let (($x823 (= x_1_2 x_2_3)))
 (not (and $x823 $x824 $x825 $x826)))))))
(assert
 (>= x_0_4 0))
(assert
 (< x_0_4 8))
(assert
 (>= y_0_4 0))
(assert
 (< y_0_4 8))
(assert
 (not (and (= x_0_4 3) (= y_0_4 2))))
(assert
 (not (and (= x_0_4 3) (= y_0_4 3))))
(assert
 (not (and (= x_0_4 3) (= y_0_4 4))))
(assert
 (not (and (= x_0_4 5) (= y_0_4 5))))
(assert
 (or (and (= x_0_4 (+ x_0_3 0)) (= y_0_4 (+ y_0_3 0))) (and (= x_0_4 (+ x_0_3 1)) (= y_0_4 (+ y_0_3 0))) (and (= x_0_4 (+ x_0_3 (- 1))) (= y_0_4 (+ y_0_3 0))) (and (= x_0_4 (+ x_0_3 0)) (= y_0_4 (+ y_0_3 1))) (and (= x_0_4 (+ x_0_3 0)) (= y_0_4 (+ y_0_3 (- 1))))))
(assert
 (>= x_1_4 0))
(assert
 (< x_1_4 8))
(assert
 (>= y_1_4 0))
(assert
 (< y_1_4 8))
(assert
 (not (and (= x_1_4 3) (= y_1_4 2))))
(assert
 (not (and (= x_1_4 3) (= y_1_4 3))))
(assert
 (not (and (= x_1_4 3) (= y_1_4 4))))
(assert
 (not (and (= x_1_4 5) (= y_1_4 5))))
(assert
 (or (and (= x_1_4 (+ x_1_3 0)) (= y_1_4 (+ y_1_3 0))) (and (= x_1_4 (+ x_1_3 1)) (= y_1_4 (+ y_1_3 0))) (and (= x_1_4 (+ x_1_3 (- 1))) (= y_1_4 (+ y_1_3 0))) (and (= x_1_4 (+ x_1_3 0)) (= y_1_4 (+ y_1_3 1))) (and (= x_1_4 (+ x_1_3 0)) (= y_1_4 (+ y_1_3 (- 1))))))
(assert
 (>= x_2_4 0))
(assert
 (< x_2_4 8))
(assert
 (>= y_2_4 0))
(assert
 (< y_2_4 8))
(assert
 (not (and (= x_2_4 3) (= y_2_4 2))))
(assert
 (not (and (= x_2_4 3) (= y_2_4 3))))
(assert
 (not (and (= x_2_4 3) (= y_2_4 4))))
(assert
 (not (and (= x_2_4 5) (= y_2_4 5))))
(assert
 (or (and (= x_2_4 (+ x_2_3 0)) (= y_2_4 (+ y_2_3 0))) (and (= x_2_4 (+ x_2_3 1)) (= y_2_4 (+ y_2_3 0))) (and (= x_2_4 (+ x_2_3 (- 1))) (= y_2_4 (+ y_2_3 0))) (and (= x_2_4 (+ x_2_3 0)) (= y_2_4 (+ y_2_3 1))) (and (= x_2_4 (+ x_2_3 0)) (= y_2_4 (+ y_2_3 (- 1))))))
(assert
 (or (and (distinct x_0_4 x_1_4) true) (and (distinct y_0_4 y_1_4) true)))
(assert
 (let (($x1026 (= y_1_3 y_0_4)))
 (let (($x1025 (= x_1_3 x_0_4)))
 (let (($x1024 (= y_0_3 y_1_4)))
 (let (($x1023 (= x_0_3 x_1_4)))
 (not (and $x1023 $x1024 $x1025 $x1026)))))))
(assert
 (or (and (distinct x_0_4 x_2_4) true) (and (distinct y_0_4 y_2_4) true)))
(assert
 (let (($x1040 (= y_2_3 y_0_4)))
 (let (($x1039 (= x_2_3 x_0_4)))
 (let (($x1038 (= y_0_3 y_2_4)))
 (let (($x1037 (= x_0_3 x_2_4)))
 (not (and $x1037 $x1038 $x1039 $x1040)))))))
(assert
 (or (and (distinct x_1_4 x_2_4) true) (and (distinct y_1_4 y_2_4) true)))
(assert
 (let (($x1054 (= y_2_3 y_1_4)))
 (let (($x1053 (= x_2_3 x_1_4)))
 (let (($x1052 (= y_1_3 y_2_4)))
 (let (($x1051 (= x_1_3 x_2_4)))
 (not (and $x1051 $x1052 $x1053 $x1054)))))))
(assert
 (>= x_0_5 0))
(assert
 (< x_0_5 8))
(assert
 (>= y_0_5 0))
(assert
 (< y_0_5 8))
(assert
 (not (and (= x_0_5 3) (= y_0_5 2))))
(assert
 (not (and (= x_0_5 3) (= y_0_5 3))))
(assert
 (not (and (= x_0_5 3) (= y_0_5 4))))
(assert
 (not (and (= x_0_5 5) (= y_0_5 5))))
(assert
 (or (and (= x_0_5 (+ x_0_4 0)) (= y_0_5 (+ y_0_4 0))) (and (= x_0_5 (+ x_0_4 1)) (= y_0_5 (+ y_0_4 0))) (and (= x_0_5 (+ x_0_4 (- 1))) (= y_0_5 (+ y_0_4 0))) (and (= x_0_5 (+ x_0_4 0)) (= y_0_5 (+ y_0_4 1))) (and (= x_0_5 (+ x_0_4 0)) (= y_0_5 (+ y_0_4 (- 1))))))
(assert
 (>= x_1_5 0))
(assert
 (< x_1_5 8))
(assert
 (>= y_1_5 0))
(assert
 (< y_1_5 8))
(assert
 (not (and (= x_1_5 3) (= y_1_5 2))))
(assert
 (not (and (= x_1_5 3) (= y_1_5 3))))
(assert
 (not (and (= x_1_5 3) (= y_1_5 4))))
(assert
 (not (and (= x_1_5 5) (= y_1_5 5))))
(assert
 (or (and (= x_1_5 (+ x_1_4 0)) (= y_1_5 (+ y_1_4 0))) (and (= x_1_5 (+ x_1_4 1)) (= y_1_5 (+ y_1_4 0))) (and (= x_1_5 (+ x_1_4 (- 1))) (= y_1_5 (+ y_1_4 0))) (and (= x_1_5 (+ x_1_4 0)) (= y_1_5 (+ y_1_4 1))) (and (= x_1_5 (+ x_1_4 0)) (= y_1_5 (+ y_1_4 (- 1))))))
(assert
 (>= x_2_5 0))
(assert
 (< x_2_5 8))
(assert
 (>= y_2_5 0))
(assert
 (< y_2_5 8))
(assert
 (not (and (= x_2_5 3) (= y_2_5 2))))
(assert
 (not (and (= x_2_5 3) (= y_2_5 3))))
(assert
 (not (and (= x_2_5 3) (= y_2_5 4))))
(assert
 (not (and (= x_2_5 5) (= y_2_5 5))))
(assert
 (or (and (= x_2_5 (+ x_2_4 0)) (= y_2_5 (+ y_2_4 0))) (and (= x_2_5 (+ x_2_4 1)) (= y_2_5 (+ y_2_4 0))) (and (= x_2_5 (+ x_2_4 (- 1))) (= y_2_5 (+ y_2_4 0))) (and (= x_2_5 (+ x_2_4 0)) (= y_2_5 (+ y_2_4 1))) (and (= x_2_5 (+ x_2_4 0)) (= y_2_5 (+ y_2_4 (- 1))))))
(assert
 (or (and (distinct x_0_5 x_1_5) true) (and (distinct y_0_5 y_1_5) true)))
(assert
 (let (($x1254 (= y_1_4 y_0_5)))
 (let (($x1253 (= x_1_4 x_0_5)))
 (let (($x1252 (= y_0_4 y_1_5)))
 (let (($x1251 (= x_0_4 x_1_5)))
 (not (and $x1251 $x1252 $x1253 $x1254)))))))
(assert
 (or (and (distinct x_0_5 x_2_5) true) (and (distinct y_0_5 y_2_5) true)))
(assert
 (let (($x1268 (= y_2_4 y_0_5)))
 (let (($x1267 (= x_2_4 x_0_5)))
 (let (($x1266 (= y_0_4 y_2_5)))
 (let (($x1265 (= x_0_4 x_2_5)))
 (not (and $x1265 $x1266 $x1267 $x1268)))))))
(assert
 (or (and (distinct x_1_5 x_2_5) true) (and (distinct y_1_5 y_2_5) true)))
(assert
 (let (($x1282 (= y_2_4 y_1_5)))
 (let (($x1281 (= x_2_4 x_1_5)))
 (let (($x1280 (= y_1_4 y_2_5)))
 (let (($x1279 (= x_1_4 x_2_5)))
 (not (and $x1279 $x1280 $x1281 $x1282)))))))
(assert
 (>= x_0_6 0))
(assert
 (< x_0_6 8))
(assert
 (>= y_0_6 0))
(assert
 (< y_0_6 8))
(assert
 (not (and (= x_0_6 3) (= y_0_6 2))))
(assert
 (not (and (= x_0_6 3) (= y_0_6 3))))
(assert
 (not (and (= x_0_6 3) (= y_0_6 4))))
(assert
 (not (and (= x_0_6 5) (= y_0_6 5))))
(assert
 (or (and (= x_0_6 (+ x_0_5 0)) (= y_0_6 (+ y_0_5 0))) (and (= x_0_6 (+ x_0_5 1)) (= y_0_6 (+ y_0_5 0))) (and (= x_0_6 (+ x_0_5 (- 1))) (= y_0_6 (+ y_0_5 0))) (and (= x_0_6 (+ x_0_5 0)) (= y_0_6 (+ y_0_5 1))) (and (= x_0_6 (+ x_0_5 0)) (= y_0_6 (+ y_0_5 (- 1))))))
(assert
 (>= x_1_6 0))
(assert
 (< x_1_6 8))
(assert
 (>= y_1_6 0))
(assert
 (< y_1_6 8))
(assert
 (not (and (= x_1_6 3) (= y_1_6 2))))
(assert
 (not (and (= x_1_6 3) (= y_1_6 3))))
(assert
 (not (and (= x_1_6 3) (= y_1_6 4))))
(assert
 (not (and (= x_1_6 5) (= y_1_6 5))))
(assert
 (or (and (= x_1_6 (+ x_1_5 0)) (= y_1_6 (+ y_1_5 0))) (and (= x_1_6 (+ x_1_5 1)) (= y_1_6 (+ y_1_5 0))) (and (= x_1_6 (+ x_1_5 (- 1))) (= y_1_6 (+ y_1_5 0))) (and (= x_1_6 (+ x_1_5 0)) (= y_1_6 (+ y_1_5 1))) (and (= x_1_6 (+ x_1_5 0)) (= y_1_6 (+ y_1_5 (- 1))))))
(assert
 (>= x_2_6 0))
(assert
 (< x_2_6 8))
(assert
 (>= y_2_6 0))
(assert
 (< y_2_6 8))
(assert
 (not (and (= x_2_6 3) (= y_2_6 2))))
(assert
 (not (and (= x_2_6 3) (= y_2_6 3))))
(assert
 (not (and (= x_2_6 3) (= y_2_6 4))))
(assert
 (not (and (= x_2_6 5) (= y_2_6 5))))
(assert
 (or (and (= x_2_6 (+ x_2_5 0)) (= y_2_6 (+ y_2_5 0))) (and (= x_2_6 (+ x_2_5 1)) (= y_2_6 (+ y_2_5 0))) (and (= x_2_6 (+ x_2_5 (- 1))) (= y_2_6 (+ y_2_5 0))) (and (= x_2_6 (+ x_2_5 0)) (= y_2_6 (+ y_2_5 1))) (and (= x_2_6 (+ x_2_5 0)) (= y_2_6 (+ y_2_5 (- 1))))))
(assert
 (or (and (distinct x_0_6 x_1_6) true) (and (distinct y_0_6 y_1_6) true)))
(assert
 (let (($x1482 (= y_1_5 y_0_6)))
 (let (($x1481 (= x_1_5 x_0_6)))
 (let (($x1480 (= y_0_5 y_1_6)))
 (let (($x1479 (= x_0_5 x_1_6)))
 (not (and $x1479 $x1480 $x1481 $x1482)))))))
(assert
 (or (and (distinct x_0_6 x_2_6) true) (and (distinct y_0_6 y_2_6) true)))
(assert
 (let (($x1496 (= y_2_5 y_0_6)))
 (let (($x1495 (= x_2_5 x_0_6)))
 (let (($x1494 (= y_0_5 y_2_6)))
 (let (($x1493 (= x_0_5 x_2_6)))
 (not (and $x1493 $x1494 $x1495 $x1496)))))))
(assert
 (or (and (distinct x_1_6 x_2_6) true) (and (distinct y_1_6 y_2_6) true)))
(assert
 (let (($x1510 (= y_2_5 y_1_6)))
 (let (($x1509 (= x_2_5 x_1_6)))
 (let (($x1508 (= y_1_5 y_2_6)))
 (let (($x1507 (= x_1_5 x_2_6)))
 (not (and $x1507 $x1508 $x1509 $x1510)))))))
(assert
 (>= x_0_7 0))
(assert
 (< x_0_7 8))
(assert
 (>= y_0_7 0))
(assert
 (< y_0_7 8))
(assert
 (not (and (= x_0_7 3) (= y_0_7 2))))
(assert
 (not (and (= x_0_7 3) (= y_0_7 3))))
(assert
 (not (and (= x_0_7 3) (= y_0_7 4))))
(assert
 (not (and (= x_0_7 5) (= y_0_7 5))))
(assert
 (or (and (= x_0_7 (+ x_0_6 0)) (= y_0_7 (+ y_0_6 0))) (and (= x_0_7 (+ x_0_6 1)) (= y_0_7 (+ y_0_6 0))) (and (= x_0_7 (+ x_0_6 (- 1))) (= y_0_7 (+ y_0_6 0))) (and (= x_0_7 (+ x_0_6 0)) (= y_0_7 (+ y_0_6 1))) (and (= x_0_7 (+ x_0_6 0)) (= y_0_7 (+ y_0_6 (- 1))))))
(assert
 (>= x_1_7 0))
(assert
 (< x_1_7 8))
(assert
 (>= y_1_7 0))
(assert
 (< y_1_7 8))
(assert
 (not (and (= x_1_7 3) (= y_1_7 2))))
(assert
 (not (and (= x_1_7 3) (= y_1_7 3))))
(assert
 (not (and (= x_1_7 3) (= y_1_7 4))))
(assert
 (not (and (= x_1_7 5) (= y_1_7 5))))
(assert
 (or (and (= x_1_7 (+ x_1_6 0)) (= y_1_7 (+ y_1_6 0))) (and (= x_1_7 (+ x_1_6 1)) (= y_1_7 (+ y_1_6 0))) (and (= x_1_7 (+ x_1_6 (- 1))) (= y_1_7 (+ y_1_6 0))) (and (= x_1_7 (+ x_1_6 0)) (= y_1_7 (+ y_1_6 1))) (and (= x_1_7 (+ x_1_6 0)) (= y_1_7 (+ y_1_6 (- 1))))))
(assert
 (>= x_2_7 0))
(assert
 (< x_2_7 8))
(assert
 (>= y_2_7 0))
(assert
 (< y_2_7 8))
(assert
 (not (and (= x_2_7 3) (= y_2_7 2))))
(assert
 (not (and (= x_2_7 3) (= y_2_7 3))))
(assert
 (not (and (= x_2_7 3) (= y_2_7 4))))
(assert
 (not (and (= x_2_7 5) (= y_2_7 5))))
(assert
 (or (and (= x_2_7 (+ x_2_6 0)) (= y_2_7 (+ y_2_6 0))) (and (= x_2_7 (+ x_2_6 1)) (= y_2_7 (+ y_2_6 0))) (and (= x_2_7 (+ x_2_6 (- 1))) (= y_2_7 (+ y_2_6 0))) (and (= x_2_7 (+ x_2_6 0)) (= y_2_7 (+ y_2_6 1))) (and (= x_2_7 (+ x_2_6 0)) (= y_2_7 (+ y_2_6 (- 1))))))
(assert
 (or (and (distinct x_0_7 x_1_7) true) (and (distinct y_0_7 y_1_7) true)))
(assert
 (let (($x1710 (= y_1_6 y_0_7)))
 (let (($x1709 (= x_1_6 x_0_7)))
 (let (($x1708 (= y_0_6 y_1_7)))
 (let (($x1707 (= x_0_6 x_1_7)))
 (not (and $x1707 $x1708 $x1709 $x1710)))))))
(assert
 (or (and (distinct x_0_7 x_2_7) true) (and (distinct y_0_7 y_2_7) true)))
(assert
 (let (($x1724 (= y_2_6 y_0_7)))
 (let (($x1723 (= x_2_6 x_0_7)))
 (let (($x1722 (= y_0_6 y_2_7)))
 (let (($x1721 (= x_0_6 x_2_7)))
 (not (and $x1721 $x1722 $x1723 $x1724)))))))
(assert
 (or (and (distinct x_1_7 x_2_7) true) (and (distinct y_1_7 y_2_7) true)))
(assert
 (let (($x1738 (= y_2_6 y_1_7)))
 (let (($x1737 (= x_2_6 x_1_7)))
 (let (($x1736 (= y_1_6 y_2_7)))
 (let (($x1735 (= x_1_6 x_2_7)))
 (not (and $x1735 $x1736 $x1737 $x1738)))))))
(assert
 (>= x_0_8 0))
(assert
 (< x_0_8 8))
(assert
 (>= y_0_8 0))
(assert
 (< y_0_8 8))
(assert
 (not (and (= x_0_8 3) (= y_0_8 2))))
(assert
 (not (and (= x_0_8 3) (= y_0_8 3))))
(assert
 (not (and (= x_0_8 3) (= y_0_8 4))))
(assert
 (not (and (= x_0_8 5) (= y_0_8 5))))
(assert
 (or (and (= x_0_8 (+ x_0_7 0)) (= y_0_8 (+ y_0_7 0))) (and (= x_0_8 (+ x_0_7 1)) (= y_0_8 (+ y_0_7 0))) (and (= x_0_8 (+ x_0_7 (- 1))) (= y_0_8 (+ y_0_7 0))) (and (= x_0_8 (+ x_0_7 0)) (= y_0_8 (+ y_0_7 1))) (and (= x_0_8 (+ x_0_7 0)) (= y_0_8 (+ y_0_7 (- 1))))))
(assert
 (>= x_1_8 0))
(assert
 (< x_1_8 8))
(assert
 (>= y_1_8 0))
(assert
 (< y_1_8 8))
(assert
 (not (and (= x_1_8 3) (= y_1_8 2))))
(assert
 (not (and (= x_1_8 3) (= y_1_8 3))))
(assert
 (not (and (= x_1_8 3) (= y_1_8 4))))
(assert
 (not (and (= x_1_8 5) (= y_1_8 5))))
(assert
 (or (and (= x_1_8 (+ x_1_7 0)) (= y_1_8 (+ y_1_7 0))) (and (= x_1_8 (+ x_1_7 1)) (= y_1_8 (+ y_1_7 0))) (and (= x_1_8 (+ x_1_7 (- 1))) (= y_1_8 (+ y_1_7 0))) (and (= x_1_8 (+ x_1_7 0)) (= y_1_8 (+ y_1_7 1))) (and (= x_1_8 (+ x_1_7 0)) (= y_1_8 (+ y_1_7 (- 1))))))
(assert
 (>= x_2_8 0))
(assert
 (< x_2_8 8))
(assert
 (>= y_2_8 0))
(assert
 (< y_2_8 8))
(assert
 (not (and (= x_2_8 3) (= y_2_8 2))))
(assert
 (not (and (= x_2_8 3) (= y_2_8 3))))
(assert
 (not (and (= x_2_8 3) (= y_2_8 4))))
(assert
 (not (and (= x_2_8 5) (= y_2_8 5))))
(assert
 (or (and (= x_2_8 (+ x_2_7 0)) (= y_2_8 (+ y_2_7 0))) (and (= x_2_8 (+ x_2_7 1)) (= y_2_8 (+ y_2_7 0))) (and (= x_2_8 (+ x_2_7 (- 1))) (= y_2_8 (+ y_2_7 0))) (and (= x_2_8 (+ x_2_7 0)) (= y_2_8 (+ y_2_7 1))) (and (= x_2_8 (+ x_2_7 0)) (= y_2_8 (+ y_2_7 (- 1))))))
(assert
 (or (and (distinct x_0_8 x_1_8) true) (and (distinct y_0_8 y_1_8) true)))
(assert
 (let (($x1938 (= y_1_7 y_0_8)))
 (let (($x1937 (= x_1_7 x_0_8)))
 (let (($x1936 (= y_0_7 y_1_8)))
 (let (($x1935 (= x_0_7 x_1_8)))
 (not (and $x1935 $x1936 $x1937 $x1938)))))))
(assert
 (or (and (distinct x_0_8 x_2_8) true) (and (distinct y_0_8 y_2_8) true)))
(assert
 (let (($x1952 (= y_2_7 y_0_8)))
 (let (($x1951 (= x_2_7 x_0_8)))
 (let (($x1950 (= y_0_7 y_2_8)))
 (let (($x1949 (= x_0_7 x_2_8)))
 (not (and $x1949 $x1950 $x1951 $x1952)))))))
(assert
 (or (and (distinct x_1_8 x_2_8) true) (and (distinct y_1_8 y_2_8) true)))
(assert
 (let (($x1966 (= y_2_7 y_1_8)))
 (let (($x1965 (= x_2_7 x_1_8)))
 (let (($x1964 (= y_1_7 y_2_8)))
 (let (($x1963 (= x_1_7 x_2_8)))
 (not (and $x1963 $x1964 $x1965 $x1966)))))))
(assert
 (>= x_0_9 0))
(assert
 (< x_0_9 8))
(assert
 (>= y_0_9 0))
(assert
 (< y_0_9 8))
(assert
 (not (and (= x_0_9 3) (= y_0_9 2))))
(assert
 (not (and (= x_0_9 3) (= y_0_9 3))))
(assert
 (not (and (= x_0_9 3) (= y_0_9 4))))
(assert
 (not (and (= x_0_9 5) (= y_0_9 5))))
(assert
 (or (and (= x_0_9 (+ x_0_8 0)) (= y_0_9 (+ y_0_8 0))) (and (= x_0_9 (+ x_0_8 1)) (= y_0_9 (+ y_0_8 0))) (and (= x_0_9 (+ x_0_8 (- 1))) (= y_0_9 (+ y_0_8 0))) (and (= x_0_9 (+ x_0_8 0)) (= y_0_9 (+ y_0_8 1))) (and (= x_0_9 (+ x_0_8 0)) (= y_0_9 (+ y_0_8 (- 1))))))
(assert
 (>= x_1_9 0))
(assert
 (< x_1_9 8))
(assert
 (>= y_1_9 0))
(assert
 (< y_1_9 8))
(assert
 (not (and (= x_1_9 3) (= y_1_9 2))))
(assert
 (not (and (= x_1_9 3) (= y_1_9 3))))
(assert
 (not (and (= x_1_9 3) (= y_1_9 4))))
(assert
 (not (and (= x_1_9 5) (= y_1_9 5))))
(assert
 (or (and (= x_1_9 (+ x_1_8 0)) (= y_1_9 (+ y_1_8 0))) (and (= x_1_9 (+ x_1_8 1)) (= y_1_9 (+ y_1_8 0))) (and (= x_1_9 (+ x_1_8 (- 1))) (= y_1_9 (+ y_1_8 0))) (and (= x_1_9 (+ x_1_8 0)) (= y_1_9 (+ y_1_8 1))) (and (= x_1_9 (+ x_1_8 0)) (= y_1_9 (+ y_1_8 (- 1))))))
(assert
 (>= x_2_9 0))
(assert
 (< x_2_9 8))
(assert
 (>= y_2_9 0))
(assert
 (< y_2_9 8))
(assert
 (not (and (= x_2_9 3) (= y_2_9 2))))
(assert
 (not (and (= x_2_9 3) (= y_2_9 3))))
(assert
 (not (and (= x_2_9 3) (= y_2_9 4))))
(assert
 (not (and (= x_2_9 5) (= y_2_9 5))))
(assert
 (or (and (= x_2_9 (+ x_2_8 0)) (= y_2_9 (+ y_2_8 0))) (and (= x_2_9 (+ x_2_8 1)) (= y_2_9 (+ y_2_8 0))) (and (= x_2_9 (+ x_2_8 (- 1))) (= y_2_9 (+ y_2_8 0))) (and (= x_2_9 (+ x_2_8 0)) (= y_2_9 (+ y_2_8 1))) (and (= x_2_9 (+ x_2_8 0)) (= y_2_9 (+ y_2_8 (- 1))))))
(assert
 (or (and (distinct x_0_9 x_1_9) true) (and (distinct y_0_9 y_1_9) true)))
(assert
 (let (($x2166 (= y_1_8 y_0_9)))
 (let (($x2165 (= x_1_8 x_0_9)))
 (let (($x2164 (= y_0_8 y_1_9)))
 (let (($x2163 (= x_0_8 x_1_9)))
 (not (and $x2163 $x2164 $x2165 $x2166)))))))
(assert
 (or (and (distinct x_0_9 x_2_9) true) (and (distinct y_0_9 y_2_9) true)))
(assert
 (let (($x2180 (= y_2_8 y_0_9)))
 (let (($x2179 (= x_2_8 x_0_9)))
 (let (($x2178 (= y_0_8 y_2_9)))
 (let (($x2177 (= x_0_8 x_2_9)))
 (not (and $x2177 $x2178 $x2179 $x2180)))))))
(assert
 (or (and (distinct x_1_9 x_2_9) true) (and (distinct y_1_9 y_2_9) true)))
(assert
 (let (($x2194 (= y_2_8 y_1_9)))
 (let (($x2193 (= x_2_8 x_1_9)))
 (let (($x2192 (= y_1_8 y_2_9)))
 (let (($x2191 (= x_1_8 x_2_9)))
 (not (and $x2191 $x2192 $x2193 $x2194)))))))
(assert
 (>= x_0_10 0))
(assert
 (< x_0_10 8))
(assert
 (>= y_0_10 0))
(assert
 (< y_0_10 8))
(assert
 (not (and (= x_0_10 3) (= y_0_10 2))))
(assert
 (not (and (= x_0_10 3) (= y_0_10 3))))
(assert
 (not (and (= x_0_10 3) (= y_0_10 4))))
(assert
 (not (and (= x_0_10 5) (= y_0_10 5))))
(assert
 (or (and (= x_0_10 (+ x_0_9 0)) (= y_0_10 (+ y_0_9 0))) (and (= x_0_10 (+ x_0_9 1)) (= y_0_10 (+ y_0_9 0))) (and (= x_0_10 (+ x_0_9 (- 1))) (= y_0_10 (+ y_0_9 0))) (and (= x_0_10 (+ x_0_9 0)) (= y_0_10 (+ y_0_9 1))) (and (= x_0_10 (+ x_0_9 0)) (= y_0_10 (+ y_0_9 (- 1))))))
(assert
 (>= x_1_10 0))
(assert
 (< x_1_10 8))
(assert
 (>= y_1_10 0))
(assert
 (< y_1_10 8))
(assert
 (not (and (= x_1_10 3) (= y_1_10 2))))
(assert
 (not (and (= x_1_10 3) (= y_1_10 3))))
(assert
 (not (and (= x_1_10 3) (= y_1_10 4))))
(assert
 (not (and (= x_1_10 5) (= y_1_10 5))))
(assert
 (or (and (= x_1_10 (+ x_1_9 0)) (= y_1_10 (+ y_1_9 0))) (and (= x_1_10 (+ x_1_9 1)) (= y_1_10 (+ y_1_9 0))) (and (= x_1_10 (+ x_1_9 (- 1))) (= y_1_10 (+ y_1_9 0))) (and (= x_1_10 (+ x_1_9 0)) (= y_1_10 (+ y_1_9 1))) (and (= x_1_10 (+ x_1_9 0)) (= y_1_10 (+ y_1_9 (- 1))))))
(assert
 (>= x_2_10 0))
(assert
 (< x_2_10 8))
(assert
 (>= y_2_10 0))
(assert
 (< y_2_10 8))
(assert
 (not (and (= x_2_10 3) (= y_2_10 2))))
(assert
 (not (and (= x_2_10 3) (= y_2_10 3))))
(assert
 (not (and (= x_2_10 3) (= y_2_10 4))))
(assert
 (not (and (= x_2_10 5) (= y_2_10 5))))
(assert
 (or (and (= x_2_10 (+ x_2_9 0)) (= y_2_10 (+ y_2_9 0))) (and (= x_2_10 (+ x_2_9 1)) (= y_2_10 (+ y_2_9 0))) (and (= x_2_10 (+ x_2_9 (- 1))) (= y_2_10 (+ y_2_9 0))) (and (= x_2_10 (+ x_2_9 0)) (= y_2_10 (+ y_2_9 1))) (and (= x_2_10 (+ x_2_9 0)) (= y_2_10 (+ y_2_9 (- 1))))))
(assert
 (or (and (distinct x_0_10 x_1_10) true) (and (distinct y_0_10 y_1_10) true)))
(assert
 (let (($x2394 (= y_1_9 y_0_10)))
 (let (($x2393 (= x_1_9 x_0_10)))
 (let (($x2392 (= y_0_9 y_1_10)))
 (let (($x2391 (= x_0_9 x_1_10)))
 (not (and $x2391 $x2392 $x2393 $x2394)))))))
(assert
 (or (and (distinct x_0_10 x_2_10) true) (and (distinct y_0_10 y_2_10) true)))
(assert
 (let (($x2408 (= y_2_9 y_0_10)))
 (let (($x2407 (= x_2_9 x_0_10)))
 (let (($x2406 (= y_0_9 y_2_10)))
 (let (($x2405 (= x_0_9 x_2_10)))
 (not (and $x2405 $x2406 $x2407 $x2408)))))))
(assert
 (or (and (distinct x_1_10 x_2_10) true) (and (distinct y_1_10 y_2_10) true)))
(assert
 (let (($x2422 (= y_2_9 y_1_10)))
 (let (($x2421 (= x_2_9 x_1_10)))
 (let (($x2420 (= y_1_9 y_2_10)))
 (let (($x2419 (= x_1_9 x_2_10)))
 (not (and $x2419 $x2420 $x2421 $x2422)))))))
(assert
 (>= x_0_11 0))
(assert
 (< x_0_11 8))
(assert
 (>= y_0_11 0))
(assert
 (< y_0_11 8))
(assert
 (not (and (= x_0_11 3) (= y_0_11 2))))
(assert
 (not (and (= x_0_11 3) (= y_0_11 3))))
(assert
 (not (and (= x_0_11 3) (= y_0_11 4))))
(assert
 (not (and (= x_0_11 5) (= y_0_11 5))))
(assert
 (or (and (= x_0_11 (+ x_0_10 0)) (= y_0_11 (+ y_0_10 0))) (and (= x_0_11 (+ x_0_10 1)) (= y_0_11 (+ y_0_10 0))) (and (= x_0_11 (+ x_0_10 (- 1))) (= y_0_11 (+ y_0_10 0))) (and (= x_0_11 (+ x_0_10 0)) (= y_0_11 (+ y_0_10 1))) (and (= x_0_11 (+ x_0_10 0)) (= y_0_11 (+ y_0_10 (- 1))))))
(assert
 (>= x_1_11 0))
(assert
 (< x_1_11 8))
(assert
 (>= y_1_11 0))
(assert
 (< y_1_11 8))
(assert
 (not (and (= x_1_11 3) (= y_1_11 2))))
(assert
 (not (and (= x_1_11 3) (= y_1_11 3))))
(assert
 (not (and (= x_1_11 3) (= y_1_11 4))))
(assert
 (not (and (= x_1_11 5) (= y_1_11 5))))
(assert
 (or (and (= x_1_11 (+ x_1_10 0)) (= y_1_11 (+ y_1_10 0))) (and (= x_1_11 (+ x_1_10 1)) (= y_1_11 (+ y_1_10 0))) (and (= x_1_11 (+ x_1_10 (- 1))) (= y_1_11 (+ y_1_10 0))) (and (= x_1_11 (+ x_1_10 0)) (= y_1_11 (+ y_1_10 1))) (and (= x_1_11 (+ x_1_10 0)) (= y_1_11 (+ y_1_10 (- 1))))))
(assert
 (>= x_2_11 0))
(assert
 (< x_2_11 8))
(assert
 (>= y_2_11 0))
(assert
 (< y_2_11 8))
(assert
 (not (and (= x_2_11 3) (= y_2_11 2))))
(assert
 (not (and (= x_2_11 3) (= y_2_11 3))))
(assert
 (not (and (= x_2_11 3) (= y_2_11 4))))
(assert
 (not (and (= x_2_11 5) (= y_2_11 5))))
(assert
 (or (and (= x_2_11 (+ x_2_10 0)) (= y_2_11 (+ y_2_10 0))) (and (= x_2_11 (+ x_2_10 1)) (= y_2_11 (+ y_2_10 0))) (and (= x_2_11 (+ x_2_10 (- 1))) (= y_2_11 (+ y_2_10 0))) (and (= x_2_11 (+ x_2_10 0)) (= y_2_11 (+ y_2_10 1))) (and (= x_2_11 (+ x_2_10 0)) (= y_2_11 (+ y_2_10 (- 1))))))
(assert
 (or (and (distinct x_0_11 x_1_11) true) (and (distinct y_0_11 y_1_11) true)))
(assert
 (let (($x2622 (= y_1_10 y_0_11)))
 (let (($x2621 (= x_1_10 x_0_11)))
 (let (($x2620 (= y_0_10 y_1_11)))
 (let (($x2619 (= x_0_10 x_1_11)))
 (not (and $x2619 $x2620 $x2621 $x2622)))))))
(assert
 (or (and (distinct x_0_11 x_2_11) true) (and (distinct y_0_11 y_2_11) true)))
(assert
 (let (($x2636 (= y_2_10 y_0_11)))
 (let (($x2635 (= x_2_10 x_0_11)))
 (let (($x2634 (= y_0_10 y_2_11)))
 (let (($x2633 (= x_0_10 x_2_11)))
 (not (and $x2633 $x2634 $x2635 $x2636)))))))
(assert
 (or (and (distinct x_1_11 x_2_11) true) (and (distinct y_1_11 y_2_11) true)))
(assert
 (let (($x2650 (= y_2_10 y_1_11)))
 (let (($x2649 (= x_2_10 x_1_11)))
 (let (($x2648 (= y_1_10 y_2_11)))
 (let (($x2647 (= x_1_10 x_2_11)))
 (not (and $x2647 $x2648 $x2649 $x2650)))))))
(assert
 (and (and (= x_0_11 7) (= y_0_11 7)) (and (= x_1_11 1) (= y_1_11 7)) (and (= x_2_11 7) (= y_2_11 1))))
(check-sat)
