def create_constraint_function(lower_bound, upper_bound):
    def constraint(value):
        return lower_bound <= value <= upper_bound
    return constraint

def permutations_with_constraints(lst, constraints):
    result = []

    if len(lst) == 1:
        return [[lst[0]]]

    for i in range(len(lst)):
        n = lst.pop(0)
        perms = permutations_with_constraints(lst, constraints)

        for perm in perms:
            # Check constraints before appending the current element
            valid = all(constraints[index](n) for index in constraints.keys())
            if valid:
                result.append([n] + perm)
        
        for index in constraints.keys():
            print(f"Checking constraint for index {index}, value {n}: {constraints[index](n)}")


        lst.append(n)

    return result

def parse_constraints(constraints_info):
    constraints = {}
    for constraint_info in constraints_info:
        parts = constraint_info.split(': ')
        index = int(parts[0])
        bounds = eval(parts[1])  # Safely evaluate the tuple
        constraints[index] = create_constraint_function(*bounds)
    return constraints

constraints_info = ['3: (1.0, 3.0)', '4: (7.0, 2.0)', '5: (0.0, 5.0)', '6: (5.0, 6.0)']

# Parse constraints
constraints = parse_constraints(constraints_info)

# Example list for permutations
my_list = [2, 3, 5, 6]

# Get permutations with constraints
result = permutations_with_constraints(my_list, constraints)

# Print the result
print(result)
