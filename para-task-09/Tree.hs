import Prelude hiding (lookup)

-- Реализовать двоичное дерево поиска без балансировки (4 балла)
data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

-- “Ord k =>” требует, чтобы элементы типа k можно было сравнивать
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup key (Node k v left right) | key == k = Just v
                                 | key < k = lookup key left
                                 | key > k = lookup key right
lookup _ _ = Nothing

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert key val (Node k v l r) | key == k = Node key val l r
                              | key < k = Node k v (insert key val l) r
                              | key > k = Node k v l (insert key val r)
insert key val _ = Node key val Nil Nil

merge :: Ord k => BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge left (Node k v l r) = Node k v (merge left l) r
merge left _ = left

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete key (Node k v l r) | key == k = merge l r
                          | key < k = Node k v (delete key l) r
                          | key > k = Node k v l (delete key r)
delete key _ = Nil
