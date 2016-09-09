# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    for i in range(len(lst) - 2,  - 1, -1):
        if lst[i] == lst[i + 1]:
            lst.pop(i + 1)
    print(lst)

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    lst = []
    j = 0
    k = 0
    for dummy_i in range(len(lst1) + len(lst2)):
        # if the second list is exhausted or ...
        if (k == len(lst2)) or (lst1[j] <= lst2[k]):
            lst.append(lst1[j])
            j += 1
        else:
            lst.append(lst2[k])
            k += 1
    print(lst)
