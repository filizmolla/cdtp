import numpy as np

def euclidean_distance(p, q):
    return np.sqrt(np.sum((p - q)**2))

def is_valid_sequence(sequence, boundaries):
    for i in range(len(sequence)):
        if not boundaries[i][0] <= sequence[i] <= boundaries[i][1]:
            return False
    return True

def select_valid_sequence(possible_sequences, original_sequence, boundaries):
    distances = [euclidean_distance(original_sequence, seq) for seq in possible_sequences]

    valid_sequences = [seq for seq in possible_sequences if is_valid_sequence(seq, boundaries)]

    if not valid_sequences:
        raise ValueError("No valid sequences found.")

    min_distance = min(distances)
    min_distance_indices = [i for i, dist in enumerate(distances) if dist == min_distance]

    selected_sequence_index = np.random.choice(min_distance_indices)
    return valid_sequences[selected_sequence_index]

# Example data
Pw_new = np.array([1.33, 5, 2.11, 3.77, 3.55, 5.45, 6.89, 8.78, 8.11])
P1 = np.array([1, 5, 2, 4, 3, 6, 7, 9, 8])
P2 = np.array([1, 5, 2, 4, 6, 3, 7, 9, 8])
P3 = np.array([1, 5, 2, 3, 4, 6, 7, 9, 8])
P4 = np.array([1, 5, 2, 3, 6, 4, 7, 9, 8])

# Define boundaries for each position in the sequence
# Example boundaries: [(1, 5), (1, 6), (2, 3), (3, 6), (4, 5), ...]
boundaries = [(1, 5)] * len(Pw_new)

# Select a valid sequence
selected_sequence = select_valid_sequence([P1, P2, P3, P4], Pw_new, boundaries)

print("Selected Valid Sequence:", selected_sequence)
