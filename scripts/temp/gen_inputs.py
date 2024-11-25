



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
#USAGE: 


def gen_inputs(out_path, in_path,number_images, number_inputs, cmpt_t, reset_t,trans_t):
    imagess = np.zeros((5*number_images, number_inputs))
    levels = np.zeros((number_images, number_inputs))
    CLR_s=np.zeros(5*number_images)
    times = np.zeros(5*number_images)
    times_rst = np.zeros(5*number_images)
    for i in range(number_images):
        folder_name = f"{in_path}/image_{i}"
        INA=[]
        print(f"{folder_name}/image.txt")
        with open(f"{folder_name}/image.txt", "r") as file:
            for line in file:
                value = line.strip()
                INA.append(value)
        for j in range(number_inputs):
            imagess[i][j] = INA[j]
        
    for i in range(number_images):
        for j in range(number_inputs):
            levels[5*i][j] = 0
            levels[5*i+1][j] = 0
            levels[5*i+2][j] = imagess[i][j]
            levels[5*i+3][j] = imagess[i][j]
            levels[5*i+4][j] = 0

            times[5*i] = (cmpt_t + reset_t +trans_t)*i
            times[5*i+1] = (cmpt_t + reset_t +trans_t)*i + reset_t - trans_t/2
            times[5*i+2] = (cmpt_t + reset_t +trans_t)*i + reset_t + trans_t/2
            times[5*i+3] = (cmpt_t + reset_t +trans_t)*i + reset_t+cmpt_t
            times[5*i+4] = (cmpt_t + reset_t+trans_t)*i + reset_t+cmpt_t+trans_t



            CLR_s[5*i] = 0.6
            CLR_s[5*i+1] = 0
            CLR_s[5*i+2] = 0
            CLR_s[5*i+3] = 0.6
            CLR_s[5*i+4] = 0.6

            times_rst[5*i] = (cmpt_t + reset_t+trans_t)*i
            times_rst[5*i+1] = (cmpt_t + reset_t+trans_t)*i + trans_t
            times_rst[5*i+2] = (cmpt_t + reset_t+trans_t)*i + reset_t - trans_t
            times_rst[5*i+3] = (cmpt_t + reset_t+trans_t)*i + reset_t
            times_rst[5*i+4] = (cmpt_t + reset_t+trans_t)*i + reset_t+cmpt_t+reset_t




    #generate a file for each input
    for i in range(number_inputs):
        with open(f"{out_path}/input_{i}.txt", "w") as file:
            for j in range(5*number_images):
                file.write(f"{times[j]} {levels[j][i]}\n")

    with open(f"{out_path}/CLR.txt", "w") as file:
        for j in range(5*number_images):
            file.write(f"{times[j]} {CLR_s[j]}\n")



if __name__ == "__main__":
    print("ERROR: Should be called as module")
        
