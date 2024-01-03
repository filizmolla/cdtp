from itertools import permutations

def is_within_constraints(value, constraint):
    lower_limit, upper_limit = min(constraint), max(constraint)
    return lower_limit <= value <= upper_limit

def permutations_with_constraints(lst, constraints):
    if not lst or len(lst) != len(constraints):
        return []

    valid_permutations = []

    for perm in permutations(lst):
        valid = all(is_within_constraints(float(perm[i]), constraints[i]) for i in range(len(perm)))
        if valid:
            valid_permutations.append(list(perm))

    return valid_permutations


my_list2 = [3, 4, 5, 6]
my_constraints2 = [(5, 5), (2, 4), (8, 3), (1, 6)]

result2 = permutations_with_constraints(my_list2, my_constraints2)

print(result2)
