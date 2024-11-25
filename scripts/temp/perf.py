import csv
import numpy as np
# CSV file
csv_file = "labels.csv"

# Initialize arrays for each column
nn_labels = []
simulation_labels = []
labels = []

# Open the CSV file
with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header
    next(reader, None)
    for row in reader:
        nn_label, sim_label, label = map(float, row)
        # Append values to respective arrays
        nn_labels.append(nn_label)
        simulation_labels.append(sim_label)
        labels.append(label)

sim=sum(np.equal(nn_labels,simulation_labels))/len(nn_labels)
NN_acc=sum(np.equal(nn_labels,labels))/len(nn_labels)
sim_acc=sum(np.equal(simulation_labels,labels))/len(nn_labels)
print(f"NN accuracy: {NN_acc}")
print(f"Simulation accuracy: {sim_acc}")
print(f"Simulation accuracy compared to NN: {sim}")


