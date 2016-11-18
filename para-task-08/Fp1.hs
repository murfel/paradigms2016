-- 1. head' возвращает первый элемент непустого списка (0,5 балла)
head' :: [a] -> a
head' (x:_) = x

-- 2. tail' возвращает список без первого элемента, для пустого - пустой (0,5)
tail' :: [a] -> [a]
tail' [] = []
tail' (_:xs) = xs

-- 3. take' возвращает первые n >= 0 элементов исходного списка (0,5)
take' :: Int -> [a] -> [a]
take' n [] = []
take' 0 s = []
take' n (x:xs) = [x] ++ take' (n - 1) xs

-- 4. drop' возвращает список без первых n >= 0 элементов; если n больше длины
-- списка, то пустой список. (0,5)
drop' :: Int -> [a] -> [a]
drop' 0 s = s
drop' n [] = []
drop' n (x:xs) = drop' (n - 1) xs

-- 5. filter' возвращает список из элементов, для которых f возвращает True (0,5)
filter' :: (a -> Bool) -> [a] -> [a]
filter' f [] = []
filter' f (x:xs) = if f x
                   then [x] ++ (filter' f xs)
                   else (filter' f xs)

-- 6. foldl' последовательно применяет функцию f к элементу списка l и значению, полученному на предыдущем шаге, начальное значение z (0,5)
-- foldl' (+) 0 [1, 2, 3] == (((0 + 1) + 2) + 3)
-- foldl' (*) 4 [] == 4
foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs

-- 7. concat' принимает на вход два списка и возвращает их конкатенацию (0,5)
-- concat' [1,2] [3] == [1,2,3]
concat' :: [a] -> [a] -> [a]
concat' [] s2 = s2
concat' s1 s2 = concat' (init s1) (last s1 : s2)


-- 8. quickSort' возвращает его отсортированный список (0,5)
quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = quickSort' left ++ [x] ++ quickSort' right
                    where left = filter' (\y -> y <= x) xs
                          right = filter' (\y -> y >= x) xs
