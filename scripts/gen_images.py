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
from model_train_eval import NeuralNetwork
# %%
def gen_images(path,number):
    # Load the MNIST dataset
    transform=transforms.Compose([
            transforms.ToTensor(),
            #transforms.Normalize((0.1307,), (0.3081,))
            ])
    train_dataset = datasets.MNIST(root='../data', train=True, download=True,transform=transform)
    test_dataset = datasets.MNIST(root='../data', train=False, download=True,transform=transform)

    num_epochs = 5
    learning_rate = 0.1



    # %%

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
    #device=torch.device("cuda")
    model = NeuralNetwork().to("cpu")
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    model.load_state_dict(torch.load('mnist_model.pth',map_location=torch.device('cpu')))
    #data loader
    batch_size = 512
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    # biases=[-1.3688758611679077 ,1.3926945924758911,0.6384987235069275,-0.8258427381515503,0.5070940852165222,3.386287212371826,-0.8813953399658203,1.999445915222168,-2.2094967365264893,-0.5659198760986328]
    model.to("cpu")
    for i in range(number):
        #create a folder for each image
        folder_name = f"{path}/image_{i}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        random_image, random_label = test_dataset[i]
        random_image=np.array(random_image.flatten())
        for j in range(len(random_image)):
            if random_image[j] < 0:
                random_image[j] = 0
            if random_image[j] > 1:
                print("############## SUPP TO 1 ##############")
        with open(f"{folder_name}/image.txt", "w") as f:
            # f.write("4e-6\n")
            f.write("0\n")
            for l in range(215):
                f.write("0\n")
            j=0
            while (j<784):
                f.write(f"{random_image[j]:.10f}e-6\n")
                j+=1
        random_image= torch.Tensor(np.array(random_image.flatten()))
        prediction = model(random_image)
        predicted_label = torch.argmax(prediction).item()
        #save the image as png
        # plt.imshow(random_image.cpu().numpy().reshape(28, 28), cmap='gray')
        # plt.savefig(f"{folder_name}/image.png")
        #save the label
        with open(f"{folder_name}/label.txt", "w") as f:
            f.write(f"{random_label}\n")
        #save the prediction
        with open(f"{folder_name}/prediction.txt", "w") as f:
            f.write(f"{predicted_label}\n")
            f.write(f"{prediction}\n")




if __name__ == "__main__":
    gen_images("./data",100)








