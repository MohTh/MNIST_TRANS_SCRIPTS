



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
#USAGE: python main.py <output_folder_path> <number_of_images>  <t/nt> <input netlist path>


def main(test, test2):
    print(f"First argument{test}")
    print(f"Second arguemnt{test2}")



if __name__ == "__main__":
    if len(sys.argv) !=5:
        print("Usage error")
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
        gen_netlist.gen_netlist(sys.argv[1],int(sys.argv[2]),sys.argv[4])
        

