
import os
import re
import shutil
import numpy as np
import pandas as pd
import sys
#%%
def main():
    print(f"ERROR: Must be run as a script, not as a module")



if __name__ == "__main__":

    if len(sys.argv) !=2:
        print("Usage error")
        print("Usage: python3 eval.py <data_prent_folder>")
    else: 
        #open all the spectre.dc files present in the folders contained in teh data directory
        data_directory = sys.argv[1]
        NN_prediction = []
        NN_label = []
        Simulation_label = []
        Simulation_prediction = []
        Label=[]
        for folder in os.listdir(data_directory):
            folder_path = os.path.join(data_directory, folder)
            if os.path.isdir(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        if file.endswith("spectre.dc"):
                            file_path = os.path.join(root, file)
                            # Process the file as needed
                            # For example, you can open and read the file using file_path
                            Prediction = []
                            with open(file_path, "r") as f:
                                # Do something with the file
                                # Regular expression pattern to match the desired lines
                                pattern = r'I5:OUT\[(\d+)\]_n_flow\s+(-?\d+(\.\d+)?(e[-+]?\d+)?)'
                                #pattern = r'I0:210(\d+)\s+(-?\d+(\.\d+)?(e[-+]?\d+)?)'

                                # Read the file line by line
                                for line in f:
                                    # Match the pattern in each line
                                    match = re.search(pattern, line)
                                    if match:
                                        # Extract the value from the matched line
                                        value = match.group(2)
                                        # Process the value as needed
                                        value=float(value)
                                        Prediction.append(value)

                                pass
                            print(f"{root}/prediction.txt")
                            shutil.copyfile(f"{root}/prediction.txt", f"{root}/prediction_sim.txt")
                            #read the first line of the file
                            with open(f"{root}/prediction.txt", "r") as file:
                                        #read the first line
                                        line = file.readline()
                                        #extract the label
                                        label = int(line.split(" ")[0])
                                        NN_label.append(label)
                            #read label from label.txt
                            with open(f"{root}/label.txt", "r") as file:
                                                #read the first line
                                                line = file.readline()
                                                #extract the label
                                                label = int(line.split(" ")[0])
                                                Label.append(label)
                            with open(f"{root}/prediction_sim.txt", "a") as file:
                                file.write("\n \n Simulation \n")
                                #Prediction=np.array(Prediction)
                                #Prediction=np.abs(Prediction)
                                Prediction2=[-x for x in Prediction]
                                #positoin of the max value
                                #print(Prediction)
                                print(Prediction2)
                                max_index = np.argmax(Prediction2)
                                print(max_index)
                                file.write(f"{max_index}\n")
                                file.write(f"{Prediction2}\n")
                                Simulation_prediction.append(Prediction2)
                                Simulation_label.append(max_index)
        #%%

        # print(len(NN_label))
        # print(len(Simulation_label))
        # print(len(Label))


        # #%%
        # print(NN_label)
        # print(Simulation_label)
        #%%
        #export NN_label and Simulation_label and Label to csv

        df = pd.DataFrame({'NN_label': NN_label, 'Simulation_label': Simulation_label, 'Label': Label})
        df.to_csv('labels.csv', index=False)



