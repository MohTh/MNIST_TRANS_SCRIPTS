#%%
import csv
import itertools
import matplotlib.pyplot as plt
import pickle
#%%
filename = "./labels.csv"
NN = []
Sim = []

with open(filename, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        NN.append(row[0])
        Sim.append(row[1])

#%%
NNN = []
Simm = []
for i in range(len(NN)-1):
    NN[i+1]=NN[i+1].replace(' ',',')
    NN[i+1]=NN[i+1].replace('[,','[')
    NN[i+1]=NN[i+1].replace(',,',',')
    NN[i+1]=NN[i+1].replace(',,',',')
    Sim[i+1]=Sim[i+1].replace(' ',',')
    Sim[i+1]=Sim[i+1].replace('[,','[')
    Sim[i+1]=Sim[i+1].replace(',,',',')
    Sim[i+1]=Sim[i+1].replace(',,',',')
    exec('NNN.append('+NN[i+1]+')')
    exec('Simm.append('+Sim[i+1]+')')
#%%
flattened_NNN = list(itertools.chain.from_iterable(NNN))
flattened_Simm = list(itertools.chain.from_iterable(Simm))

print(len(flattened_NNN))
print(len(flattened_Simm))

#%%


# Plot Simm with respect to NNN 

plt.scatter(flattened_NNN, flattened_Simm)
plt.xlabel('NNN')
plt.ylabel('Simm')
plt.show()
#with open('INP1.plk', 'wb') as file:
#	pickle.dump(flattened_Simm,file)

#with open('NN.plk', 'wb') as file:
#	pickle.dump(flattened_NNN,file)
#%%
