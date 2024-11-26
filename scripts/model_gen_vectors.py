#%%
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
from model_train_eval import NeuralNetwork


Vmin=0.2
Vmax=1.2
Vmid=0.548
# %%
# Load the MNIST dataset
def model_gen_vectors():
    #check if file exists
    if os.path.exists('model_weights.txt'):
        os.remove('model_weights.txt')
    #check if file doesn't exist
    if not(os.path.exists('mnist_model.pth')):
        print("Model file not found")
        print("Training the model")
        model_train_eval.model_train_eval()

        
    transform=transforms.Compose([
            transforms.ToTensor(),
            #transforms.Normalize((0.1307,), (0.3081,))
            ])
    train_dataset = datasets.MNIST(root='../data', train=True, download=True,transform=transform)
    test_dataset = datasets.MNIST(root='../data', train=False, download=True,transform=transform)



    # class NeuralNetwork(torch.nn.Module):
    #     def __init__(self):
    #         super(NeuralNetwork, self).__init__()
    #         # self.hidden_layer = torch.nn.Linear(784, 1000)  # One hidden layer with 10 neurons
    # #        self.hidden_layer2 = torch.nn.Linear(1024, 2000)  # One hidden layer with 10 neurons
    # #        self.hidden_layer3 = torch.nn.Linear(2000, 784)  # One hidden layer with 10 neurons
    # #        self.hidden_layer4 = torch.nn.Linear(2000, 128)  # One hidden layer with 10 neurons
    #         self.output_layer = torch.nn.Linear(784, 10)  # Output layer with 1 neuron

    #     def forward(self, x):
    #         # x = torch.relu(self.hidden_layer(x))
    #         # x = torch.relu(self.hidden_layer2(x))
    #         # x = torch.relu(self.hidden_layer3(x))
    # #        x = torch.relu(self.hidden_layer4(x))
    #         x = (self.output_layer(x))
    #         return x

    # Create an instance of the neural network
    # device=torch.device("cuda")
    model = NeuralNetwork().to("cpu")

    model.load_state_dict(torch.load('mnist_model.pth',map_location=torch.device('cpu')))
    model.to("cpu")

    # Extract and flatten the weights
    weights_list = []
    for param_tensor in model.state_dict():
        weights = model.state_dict()[param_tensor].numpy()
        weights_list.extend(weights)

    # Save the weights to a text file
    with open('model_weights.txt', 'w') as f:
        for weight in weights_list:
            f.write(f'{weight}\n')
    weights=[]
    # Open the text file
    with open('model_weights.txt', 'r') as file:
        # Read the entire content of the file
        content = file.read().replace("\n", "")

        # Split the content into strings using "]" as a separator
        strings = content.split("]")

        # Process each string
        for string in strings:
            # If the string is not empty
            if string.strip():
                # Add back the "]" that was used as a separator
                string_with_separator = string.strip() + "]"
                weights.append(string_with_separator)
                # Now you can use string_with_separator as needed
                # print("String with separator:", string_with_separator)



    # BIASES 

    # biases=[-1.4442347288131714,1.4510644674301147,0.5770558714866638,-0.6696855425834656,0.3050135374069214,3.3007800579071045,-0.8144980072975159,1.7442504167556763,-1.7945587635040283,-0.45903870463371277]
    # biase=np.abs(biases)
    # do=[]
    # for i in range(10):
        # biase[i]=biase[i]*3.4e-6
        # print(biase[i])
        # do.append((np.log(biase[i]/(0.32403826878033107*4e-6))/-1.5269379457153966)+0.5666365493690164)
    # for it in range(10):
        # do[it] = 1.2 - do[it]
        # if do[it] < 0.7:
        #     do[it] = 0.7
        # elif do[it] > 1.8:
        #     do[it] = 1.8

    weightss=[]
    for i in range(10):
        weights[i]=weights[i].replace(" ",",")
        weights[i]=weights[i].replace("[,","[")
        weights[i]=weights[i].replace(",,,",",")
        weights[i]=weights[i].replace(",,",",")
        weights[i]=weights[i].replace(",,",",")
        weights[i]=weights[i].replace(",,",",")
        weights[i]=weights[i].replace(".,",",")
        weights[i]=weights[i].replace("[,","[")
        exec('temp='+weights[i],globals())
        weightss.append(temp)

    Vb=[]
    weightss=np.array(weightss)
    under=0
    over=0
    for i in range(10):
        for j in range(len(weightss[i])):
            iiiiii=0
            # if weightss[i][j] == 0:
            #     weightss[i][j] = 1e-10    
        else:
            # print(np.abs((weightss[i])))
            Vb.append(-np.log(2+weightss[i]/np.max(np.abs(weightss)))*(Vmax-Vmin)+Vmin+np.log(3))
            # Vb.append(((np.log((np.abs((weightss[i]))/0.2438286373e-2))/(-1.82693795))+0.266365493690164)/3+0.6)
        for j in range(len(Vb[i])):
            if Vb[i][j] < Vmin:
                Vb[i][j] = Vmin
                under+=1
                print(f"Warning: ############### Vb[{i}][{j}]: {Vb[i][j]} < Vmin , weight: {weightss[i][j]} ###########")
            elif Vb[i][j] > Vmax:
                Vb[i][j] = Vmax
                over+=1
                print(f"Warning: ############### Vb[{i}][{j}]: {Vb[i][j]} > Vmax , weight: {weightss[i][j]} ###########")
    # Vb_capped = np.clip(Vb, Vmin, Vmax)
    print(f"Under: {under}")
    print(f"Over: {over}")
    
    INBP=np.zeros((10,784))
    INBN=np.zeros((10,784))
    for i in range(10):
        for j in range(len(weightss[i])):
            #if weightss[i][j] < 0:
                INBP[i][j]=(Vb[i][j])
                # print(INBP[i][j])
                INBN[i][j]=(Vmid)
            #else:
                # INBP[i][j]=(Vb[i][j])
                # INBN[i][j]=(Vmax)
    with open('INBP3.txt', 'w') as f:
        j=0   
        for i in range(10):
            # if biases[i] < 0:
            #     f.write(f"{Vmax}\n")
            # else :
            #     # f.write("%s\n"% do[i])
            f.write(f"{Vmid}\n")
            for l in range(215):
                f.write(f"{Vmid}\n")
            j=0
            while (j<784):
                f.write("%s\n" % INBP[i][j])
                j+=1
    with open('INBN3.txt', 'w') as f:
        j=0
        for i in range(10):
            # if biases[i] < 0:
            #     # f.write("%s\n" % do[i])
            #     f.write(f"{Vmax}\n")
            # else :
            f.write(f"{Vmid}\n")
            for l in range(215):
                f.write(f"{Vmid}\n")
            j=0
            while (j<784):
                f.write("%s\n" % INBN[i][j])
                j+=1



if __name__ == "__main__":
    model_gen_vectors()
