import re
from collections import defaultdict
import csv

# File path
file_path = "./psf/tran.tran.tran"
output_file_path = "./tran.csv"

# Data storage
time_values = []
current_data = defaultdict(list)

# Regular expressions for matching
time_pattern = re.compile(r'"time"\s+([+-]?\d+\.?\d*e[+-]?\d+)')
current_pattern = re.compile(r'"I0:(\d+)"\s+([+-]?\d+\.?\d*e[+-]?\d+)')

# Read and parse the file
with open(file_path, 'r') as file:
    for line in file:
        # Match time
        time_match = time_pattern.match(line)
        if time_match:
            time_values.append(float(time_match.group(1)))
            continue

        # Match current values
        current_match = current_pattern.match(line)
        if current_match:
            identifier = current_match.group(1)
            value = float(current_match.group(2))
            current_data[identifier].append(value)

# Convert the defaultdict to a regular dictionary for easier handling
current_data = dict(current_data)

# Prepare data for writing to CSV
headers = ["time"] + [f"I0:{key}" for key in sorted(current_data.keys())]
rows = []

# Make sure all arrays are the same length by padding with empty values
num_rows = len(time_values)
for i in range(num_rows):
    row = [time_values[i]]
    for key in sorted(current_data.keys()):
        row.append(current_data[key][i] if i < len(current_data[key]) else "")
    rows.append(row)


with open(output_file_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headers)  # Write header row
    writer.writerows(rows)    # Write data rows
    
    
    
    
    
    
    
    
# Print results for verification
#print("Time values:")
#print(time_values)
#print("\nCurrent values for each I0:XXXX:")
#for key, values in current_data.items():
#    print(f"I0:{key} -> {values}")
#    break
