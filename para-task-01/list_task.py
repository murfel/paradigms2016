# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    new_lst = []
    if len(lst) != 0:
        new_lst.append(lst[0])

    for i in range(1, len(lst)):
        if lst[i] != new_lst[-1]:
            new_lst.append(lst[i])

    return new_lst

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    lst = []
    j = 0
    k = 0
    for _ in range(len(lst1) + len(lst2)):
        # if the second list is exhausted or ...
        if (k == len(lst2)) or (lst1[j] <= lst2[k]):
            lst.append(lst1[j])
            j += 1
        else:
            lst.append(lst2[k])
            k += 1
    return lst
