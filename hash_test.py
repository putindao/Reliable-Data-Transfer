from hash import calculate_file_hash

print("Original:")
print(calculate_file_hash("image.jpg"))

print()

print("Received:")
print(calculate_file_hash("received.jpg"))