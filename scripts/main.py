



import torch
import numpy as np
import matplotlib.pyplot as plt
import math
from torchvision import datasets,transforms
import torch.nn as nn
from torch.utils.data import Dataset
import os
from json import JSONEncoder
import json
import model_train_eval
import sys
import os
import model_train_eval
import model_gen_vectors
import gen_images
import gen_netlist
import configparser
import re
import gen_inputs
#USAGE: python main.py <output_folder_path> <number_of_images>  <t/nt>



dk_config = "./pdk/gpdk180"

config=configparser.ConfigParser()
config.read('./config.txt')
cmpt_t=config.get('DEFAULT','cmpt_t')
reset_t=config.get('DEFAULT','reset_t')
trans_t=config.get('DEFAULT','trans_t')
CAP=config.get('DEFAULT','cap')




def main(test, test2):
    print(f"First argument{test}")
    print(f"Second arguemnt{test2}")



if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Usage error")
        print("Usage: python main.py <output_folder_path> <number_of_images>  <t/nt>")
    else: 
        if not(os.path.exists('mnist_model.pth')):
            print("Model file not found")
            print("Training the model")
            model_train_eval.model_train_eval()
        elif sys.argv[3] == "t":
            print("Re-training the model")
            model_train_eval.model_train_eval()
        model_gen_vectors.model_gen_vectors()
        #check if folder exists and delete it
        if os.path.exists(sys.argv[1]):
            os.system(f"rm -r {sys.argv[1]}")
        gen_images.gen_images(sys.argv[1],int(sys.argv[2]))
        gen_inputs.gen_inputs("./stimul",sys.argv[1], int(sys.argv[2]),1000,float(cmpt_t),float(reset_t),float(trans_t))
        gen_netlist.gen_netlist(sys.argv[1],int(sys.argv[2]),CAP,dk_config)

        # Path to your text file
        file_path = f"{sys.argv[1]}/netlist"

        # New value for stop
        new_stop_value = f"{((float(cmpt_t) + float(reset_t)+float(trans_t))*int(sys.argv[2]))}"
        # Read the file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Modify the stop value
        with open(file_path, "w") as file:
            for line in lines:
                if "stop=" in line:
                    # Split the line and replace the stop value
                    parts = line.split(" ")
                    for i, part in enumerate(parts):
                        if part.startswith("stop="):
                            parts[i] = f"stop={new_stop_value}"
                            break
                    # Join the line back together
                    line = " ".join(parts)
                
                file.write(line)

        print(f"The value of 'stop' has been updated to {new_stop_value}.")
        

