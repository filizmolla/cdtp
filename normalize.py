def normalize_numbers_to_range_int(numbers, new_min, new_max):
    # Find the minimum and maximum values in the array
    min_value = min(numbers)
    max_value = max(numbers)
    
    # Calculate the range of values
    value_range = max_value - min_value
    
    # Normalize each number to the new range and round to the nearest integer
    normalized_numbers = [round((num - min_value) / value_range * (new_max - new_min) + new_min) for num in numbers]
    
    return normalized_numbers

# Example usage with the provided numbers and the desired integer range [0, 5]
numbers = [1, 5, 2, 4, 4, 7, 7, 9, 8]
normalized_numbers = normalize_numbers_to_range_int(numbers, 0, 8)

print("Original numbers:", numbers)
print("Normalized numbers (0 to 5 range, integers only):", normalized_numbers)
