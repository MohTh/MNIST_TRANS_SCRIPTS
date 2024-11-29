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


class NeuralNetwork(torch.nn.Module):
        def __init__(self):
            super(NeuralNetwork, self).__init__()
            # self.hidden_layer = torch.nn.Linear(784, 1000)  # One hidden layer with 10 neurons
    #        self.hidden_layer2 = torch.nn.Linear(1024, 2000)  # One hidden layer with 10 neurons
    #        self.hidden_layer3 = torch.nn.Linear(2000, 784)  # One hidden layer with 10 neurons
    #        self.hidden_layer4 = torch.nn.Linear(2000, 128)  # One hidden layer with 10 neurons
            self.output_layer = torch.nn.Linear(784, 10,bias=False)  # Output layer with 1 neuron

        def forward(self, x):
            # x = torch.relu(self.hidden_layer(x))
            # x = torch.relu(self.hidden_layer2(x))
            # x = torch.relu(self.hidden_layer3(x))
    #        x = torch.relu(self.hidden_layer4(x))
            x = (self.output_layer(x))
            return x
        

def model_train_eval():
    # %%
    # Load the MNIST dataset
    transform=transforms.Compose([
            transforms.ToTensor(),
            #transforms.Normalize((0.1307,), (0.3081,))
            ])
    train_dataset = datasets.MNIST(root='../data', train=True, download=True,transform=transform)
    test_dataset = datasets.MNIST(root='../data', train=False, download=True,transform=transform)


    # %%

    # # Visualize some images from the dataset
    # fig, axes = plt.subplots(2, 5, figsize=(10, 4))
    # for i, ax in enumerate(axes.flat):
    #     image, label = train_dataset[2*i]
    #     print("shape before: ",image.shape)
    #     image=np.squeeze(image)
    #     print("shape after: ",image.shape)
    #     ax.imshow(image, cmap='gray')
    #     ax.set_title(f"Label: {label}")
    #     ax.axis('off')
    # plt.show()




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
    device=torch.device("cuda")
    model = NeuralNetwork().to(device)


    # %%

    #training hyperparameters
    num_epochs = 100
    learning_rate = 0.0001

    #loss and optimizer
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    #data loader
    batch_size = 128
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)
    #training the model

    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # Convert images to tensors
            
            images = torch.stack([torch.Tensor(np.abs(np.array(image.flatten()))) for image in images])
            # Convert labels to tensors
            labels = torch.tensor(labels)
            images,labels=images.to(device),labels.to(device)
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i+1) % 100 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_dataset)//batch_size}], Loss: {loss.item():.4f}')

    minn=-1
    maxx=1
    steps=64
    step=(maxx-minn)/steps
    i=-1
    stepss=[]
    while i<1:
        stepss.append(i)
        i+=step
    with torch.no_grad():
        # Access weights of the first linear layer (fc1)
        weight_fc1 = model.output_layer.weight
        bias_fc1 = model.output_layer.bias
        for i in range(len(weight_fc1)):
            for j in range(len(weight_fc1[i])):
                for ii in range(1,len(stepss)):
                    #print stepss[ii] and stepss[ii-1]
                    
                    if weight_fc1[i][j] <= stepss[ii] and weight_fc1[i][j] > stepss[ii-1]:
                        if weight_fc1[i][j] - stepss[ii-1] < stepss[ii] - weight_fc1[i][j]:
                            weight_fc1[i][j] = stepss[ii-1]
                        else:
                            weight_fc1[i][j] = stepss[ii]
                        break

        model.output_layer.weight = weight_fc1

    model.eval()
    total_correct = 0
    total_samples = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images = torch.stack([torch.Tensor(np.abs(np.array(image.flatten()))) for image in images])
            labels = torch.tensor(labels)
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            
            total_samples += labels.size(0)
            total_correct += (predicted == labels).sum().item()

    accuracy = 100 * total_correct / total_samples
    print(f'Test Accuracy: {accuracy:.2f}%')



    with torch.no_grad():
        for images, labels in train_loader:
            images = torch.stack([torch.Tensor(np.array(image.flatten())) for image in images])
            labels = torch.tensor(labels)
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            
            total_samples += labels.size(0)
            total_correct += (predicted == labels).sum().item()

    accuracy = 100 * total_correct / total_samples
    print(f'train Accuracy: {accuracy:.2f}%')

    # Save the model as txt
    torch.save(model.state_dict(), 'mnist_model.pth')



if __name__ == "__main__":
    model_train_eval()
