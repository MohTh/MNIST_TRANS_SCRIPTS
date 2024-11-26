import numpy as np
import os
import csv 


number_images=100
min_cmpt=0.5e-9
max_cmpt=5e-9
step_size=0.5e-9
trans_t=0.05e-9
reset_t=2e-9


#generate the times between min and max with step size
times = np.arange(min_cmpt,max_cmpt,step_size)
accuracies = []


for time in times: 
    print(f"Time: {time}")
    #generate the config file
    with open(f"./config.txt", "w") as file:
        file.write("[DEFAULT]\n")
        file.write(f"cmpt_t={time}\n")
        file.write(f"reset_t={reset_t}\n")
        file.write(f"trans_t={trans_t}\n")
    
    #run the simulation
    os.system(f"./simulate.sh ./dataa {number_images} nt ./netlist_1000x10")

    #read the accuracy from accuracy.txt
    with open(f"./accuracy.txt", "r") as file:
        accuracy = file.read()
        print(f"Accuracy: {accuracy}")
        accuracies.append(accuracy)
    
    print("\n")
    print("\n")
    print("########### NEXT ITERATION #############")
    print("\n")


#write the accuracies and times to a csv file
with open("accuracy.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Accuracy"])
    for i in range(len(times)):
        writer.writerow([times[i], accuracies[i]])



