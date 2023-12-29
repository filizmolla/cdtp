def has_duplicates(arr):
    seen = set()
    for elem in arr:
        if elem in seen:
            return True
        seen.add(elem)
    return False

# Example usage:
my_array = [1, 2, 3, 4, 5]  # This array has duplicates (1 is repeated)
result = has_duplicates(my_array)



if result:
    print("The array has duplicates.")
else:
    print("The array does not have duplicates.")

