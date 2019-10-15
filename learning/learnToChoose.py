import torch
import numpy as np 
from torch.utils.data import Dataset, TensorDataset, DataLoader
from torch.utils.data.dataset import random_split
import torch.nn as nn
import torch.optim as optim

device = 'cuda' if torch.cuda.is_available() else 'cpu'

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


fileIn = open("numericData_EE.txt")
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
#train_dataset, val_dataset = random_split(dataset, [100, 162]) # total 262 CR
#train_dataset, val_dataset = random_split(dataset, [200, 1504]) # total 1704 SD
train_dataset, val_dataset = random_split(dataset, [200, 2255]) # total 2455 EE
#train_dataset, val_dataset = random_split(dataset, [100, 92]) # total 192 SR
# Builds a loader for each dataset to perform mini-batch gradient descent
train_loader = DataLoader(dataset=train_dataset, batch_size=1)
val_loader = DataLoader(dataset=val_dataset, batch_size=1)

# Builds a simple sequential model
#model = nn.Sequential(nn.Linear(24, 1)).to(device) # SD
model = nn.Sequential(nn.Linear(22, 1)).to(device) # CR, EE
#model = nn.Sequential(nn.Linear(14, 1)).to(device) #SR
#model = nn.Linear(6, 2).to(device)
print(model.state_dict())

# Sets hyper-parameters
#lr = 1e-3 # SR, CR, SD
lr = 1e-4 # EE
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

def printList(l):
    for i in l:
        print(i)
#print(model.state_dict())
print("training losses ")
printList(losses)
print("validation losses")
printList(val_losses)
print(" mean training loss " , np.mean(losses))
print(" mean validation loss ", np.mean(val_losses))