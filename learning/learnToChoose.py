import torch
import numpy as np 
from torch.utils.data import Dataset, TensorDataset, DataLoader
from torch.utils.data.dataset import random_split
import torch.nn as nn
import torch.optim as optim

device = 'cpu' #if torch.cuda.is_available() else 'cpu'
domain = "EE"
modelFrom = "planner"

torch.manual_seed(100)
np.random.seed(200)

def make_train_step(model, loss_fn, optimizer):
    # Builds function that performs a step in the train loop
    def train_step(x, y):
        # Sets model to TRAIN mode
        model.train()
        # Makes predictions
        yhat = model(x)
        # Computes loss
        loss = loss_fn(y, yhat)
        # Computes gradients
        loss.backward()
        # Updates parameters and zeroes gradients
        optimizer.step()
        optimizer.zero_grad()
        # Returns the loss
        return loss.item()
    
    # Returns the function that will be called inside the train loop
    return train_step


fileIn = open("numericData_{}_{}.txt".format(domain, modelFrom))
x = []
y = []
line = fileIn.readline()
while(line != ""):
    nums = line[0:-1]
    items = nums.split(" ")
    x_row = [float(i) for i in items[0:-1]]
    x.append(x_row)
    y.append([int(items[-1])])
    line = fileIn.readline()
fileIn.close()

trainingSetSize = {
    "EE": 200,
    "SD": 200,
    "SR": 100,
    "CR": 100,
    "OF": 200,
}

validationSetSize = {
    "EE": len(x) - 200,
    "SD": len(x) - 200,
    "SR": len(x) - 100,
    "CR": len(x) - 100,
    "OF": len(x) - 200,
}

x = np.array(x)
y = np.array(y)


#x = np.random.rand(10, 3, 1)
#print(" x is ", x)
#y = 1 + .1 * np.random.randn(10, 1)

x_tensor = torch.from_numpy(x).float()
y_tensor = torch.from_numpy(y).float()


print("y_tensor is ", y_tensor)
# Builds dataset with ALL data
dataset = TensorDataset(x_tensor, y_tensor)
# Splits randomly into train and validation datasets
train_dataset, val_dataset = random_split(dataset, [trainingSetSize[domain], validationSetSize[domain]]) 
# Builds a loader for each dataset to perform mini-batch gradient descent
train_loader = DataLoader(dataset=train_dataset, batch_size=1)
val_loader = DataLoader(dataset=val_dataset, batch_size=1)

# Builds a simple sequential model

features = {
    "EE": 22,
    "SD": 24,
    "SR": 14,
    "OF": 0,
    "CR": 22,
}
model = nn.Sequential(nn.Linear(features[domain], 1)).to(device) 
print(model.state_dict())

# Sets hyper-parameters
if modelFrom == "actor":
    lrD = {
        "EE": 1e-4,
        "SD": 1e-3,
        "SR": 1e-5,
        "CR": 1e-3,
        "OF": 1e-3,
    }
else:
    lrD = {
        "EE": 1e-3,
        "SD": 1e-3,
        "SR": 1e-5,
        "CR": 1e-3,
        "OF": 1e-3,
    }
lr = lrD[domain]
n_epochs = 1

# Defines loss function and optimizer
loss_fn = nn.MSELoss(reduction='mean')
optimizer = optim.SGD(model.parameters(), lr=lr)

losses = []
val_losses = []
# Creates function to perform train step from model, loss and optimizer
train_step = make_train_step(model, loss_fn, optimizer)

# Training loop
for epoch in range(n_epochs):
    # Uses loader to fetch one mini-batch for training
    for x_batch, y_batch in train_loader:
        # NOW, sends the mini-batch data to the device
        # so it matches location of the MODEL
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        # One stpe of training
        loss = train_step(x_batch, y_batch)
        losses.append(loss)
        with torch.no_grad():
        # Uses loader to fetch one mini-batch for validation
            v = []
            for x_val, y_val in val_loader:
                # Again, sends data to same device as model
                x_val = x_val.to(device)
                y_val = y_val.to(device)
                
                # What is that?!
                model.eval()
                # Makes predictions
                yhat = model(x_val)
                # Computes validation loss
                val_loss = loss_fn(y_val, yhat)
                #print(val_loss)
                v.append(val_loss)
            val_losses.append(np.mean(v))
        
    # After finishing training steps for all mini-batches,
    # it is time for evaluation!
        
    # We tell PyTorch to NOT use autograd...
    # Do you remember why?
    #with torch.no_grad():
        # Uses loader to fetch one mini-batch for validation
        #for x_val, y_val in val_loader:
            # Again, sends data to same device as model
            #x_val = x_val.to(device)
            #y_val = y_val.to(device)
            
            # What is that?!
            #model.eval()
            # Makes predictions
            #yhat = model(x_val)
            # Computes validation loss
            #val_loss = loss_fn(y_val, yhat)
            #print(val_loss)
            #val_losses.append(val_loss.item())

import matplotlib.pyplot as plt

def GetString(depth):
    s = []
    for item in depth:
        s.append(str(item))

    return s

COLORS = ['r.-', 'g.-', 'm^-.', 'go--', 'c^:', 'rs--', 'ms--', 'gs--']

def PlotViaMatlab(x, y, c, l):
    line1, = plt.plot(x, y, c, label=l, linewidth=3, MarkerSize=1, markerfacecolor='white')

def CreatePlot(training, validation):
    plt.clf()
    font = {
        'family' : 'times',
        'weight' : 'regular',
        'size'   : 12}
    plt.rc('font', **font)

    gap = {
        "SD": 50,
        "EE": 50,
        "SR": 10,
        "CR": 10,
    }
    x = list(range(0, trainingSetSize[domain]))

    PlotViaMatlab(x,
                training,
                COLORS[0],
                'Training Loss in {} domain'.format(domain))
    PlotViaMatlab(x,
                validation,
                COLORS[1],
                'Validation Loss in {} domain'.format(domain))

    fname = 'Loss_{}_{}.png'.format(domain, modelFrom)
    plt.xlabel('Training steps')
    plt.xticks(np.arange(min(x), max(x)+10, gap[domain]))
    plt.ylabel("Loss")
    plt.legend(bbox_to_anchor=(0.3, 0.7), loc=3, ncol=1, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

def printList(l):
    for i in l:
        print(i)
#print(model.state_dict())
print("training losses ")
printList(losses)

print("validation losses")
printList(val_losses)
CreatePlot(losses, val_losses)
print(" mean training loss " , np.mean(losses))
print(" mean validation loss ", np.mean(val_losses))
torch.save(model.state_dict(), "model{}_{}".format(domain, modelFrom))