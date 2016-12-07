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
insert key val (Node k v left right) | key == k = Node key val left right
                                     | key < k = Node k v (insert key val left) right
                                     | key > k = Node k v left (insert key val right)
insert key val _ = Node key val Nil Nil

merge :: Ord k => BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge (Node k v subleft subright) right = merge (merge subleft subright) (insert k v right)
merge _ right = right

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete key (Node k v left right) | key == k = merge left right
                                 | key < k = Node k v (delete key left) right
                                 | key > k = Node k v left (delete key right)
delete key _ = Nil
