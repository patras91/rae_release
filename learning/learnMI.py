import torch
import numpy as np 
from torch.utils.data import Dataset, TensorDataset, DataLoader
from torch.utils.data.dataset import random_split
import torch.nn as nn
import torch.optim as optim
import argparse
import matplotlib.pyplot as plt

device = 'cpu' #if torch.cuda.is_available() else 'cpu'
domain = None
modelFrom = None
resultsFolder = "AIJ2020"

torch.manual_seed(100)
np.random.seed(200)

from paramInfo import *

def GetParamLearningNetworks(domain, method):
    models = {}
    for p in params[domain][method]:
        model = nn.Sequential(nn.Linear(nFeatures[domain], 128), 
            nn.ReLU(inplace=True), 
            nn.Linear(128, params[domain][method][p]))
        models[p] = model
    return models
    
def make_train_step(model, loss_fn, optimizer):
    # Builds function that performs a step in the train loop
    def train_step(x, y):
        # Sets model to TRAIN mode
        model.train()
        # Makes predictions
        yhat = model(x)
        # Computes loss
        loss = loss_fn(yhat, y)
        # Computes gradients
        loss.backward()
        # Updates parameters and zeroes gradients
        optimizer.step()
        optimizer.zero_grad()
        # Returns the loss
        return yhat, loss.item()
    
    # Returns the function that will be called inside the train loop
    return train_step

# Builds a simple sequential model

n_epochs = 10

# Defines loss function and optimizer
loss_fn = nn.CrossEntropyLoss()
tr_losses, val_losses, tr_accuracy, val_accuracy = [], [], [], []

def GetLabel(yhat):
    r, predicted = torch.max(yhat, 0)
    return predicted.long()

def GetAccValue(acc):
    return sum(acc)/len(acc)

def GetOneHotAccuracyValues(yhat, y):
    res = []
    for i1, i2 in zip(yhat, y):
        res.append(1 if GetLabel(i1) == i2 else 0)
    return res

def GetString(depth):
    return [str(item) for item in depth]

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

    fname = 'plots/AIJ2020/Loss_{}_{}.png'.format(domain, modelFrom)
    plt.xlabel('Training steps')
    plt.xticks(np.arange(min(x), max(x)+10, gap[domain]))
    plt.ylabel("Loss")
    plt.legend(bbox_to_anchor=(0.3, 0.7), loc=3, ncol=1, borderaxespad=0.)
    plt.savefig(fname, bbox_inches='tight')

def PrintList(l, fname):
    f = open(fname, "w")
    for i in l:
        f.write(str(i)+"\n")
    f.close()

#print(model.state_dict())

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['CR', 'SD', SR', EE']",
                           type=str, required=True)
    argparser.add_argument("--modelFrom", help="actor (a) or planner (p) ?",
                           type=str, required=True)
    argparser.add_argument("--nepochs", help="how many epochs (>=1) ?",
                           type=int, required=False, default = 1)
    
    args = argparser.parse_args()
    domain = args.domain
    n_epochs = args.nepochs
    modelFrom = "actor" if args.modelFrom == 'a' else "planner"

    for m in params[domain]:
        models = GetParamLearningNetworks(domain, m)
        for p in models:
            print("Training for ", m, ,p)
            fileIn = open("../../raeResults/{}/learning/{}/numericData_{}_{}_{}_{}.txt".format(resultsFolder, domain, domain, modelFrom, m, param, models[p]))
            
            x, y = [], []
            line = fileIn.readline()
    
            while(line != ""):
                items = line[0:-1].split(" ")
                x_row = [float(i) for i in items[0:-1]]
                x.append(x_row)
                y.append(int(items[-1]))
                line = fileIn.readline()
            fileIn.close()

            trainingSetSize = {
                "EE": round(0.8*len(x)),
                "SD": round(0.8*len(x)),
                "SR": round(0.8*len(x)),
                "CR": round(0.8*len(x)),
                "OF": round(0.8*len(x)),
            }

            validationSetSize = {
                "EE": len(x) - trainingSetSize["EE"],
                "SD": len(x) - trainingSetSize["SD"],
                "SR": len(x) - trainingSetSize["SR"],
                "CR": len(x) - trainingSetSize["CR"],
                "OF": len(x) - trainingSetSize["OF"],
            }

            x, y = np.array(x), np.array(y)

            x_tensor = torch.from_numpy(x).float()
            y_tensor = torch.from_numpy(y).long()

            dataset = TensorDataset(x_tensor, y_tensor)
            train_dataset, val_dataset = random_split(dataset, [trainingSetSize[domain], validationSetSize[domain]]) 
            train_loader = DataLoader(dataset=train_dataset, batch_size=100)
            val_loader = DataLoader(dataset=val_dataset, batch_size=100)


            # Sets hyper-parameters
            if modelFrom == "actor":
                lrD = {
                    "EE": 1e-2, #1e-3,
                    "SD": 1e-2, #1e-3,
                    "SR": 1e-1,
                    "CR": 1e-2,
                    "OF": 1e-3,
                }
            else:
                lrD = {
                    "EE": 1e-2, #1e-3,
                    "SD": 1e-2, #1e-3,
                    "SR": 1e-2,
                    "CR": 1e-1, #1e-1,
                    "OF": 1e-3,
                }
            lr = lrD[domain]

            optimizer = optim.SGD(model.parameters(), lr=lr)

            # Creates function to perform train step from model, loss and optimizer
            train_step = make_train_step(model, loss_fn, optimizer)

            # Training loop
            for epoch in range(n_epochs):

                vLoss1, tLoss1, vAcc1, tAcc1 = []
                # Uses loader to fetch one mini-batch for training
                
                for x_batch, y_batch in train_loader:

                    # NOW, sends the mini-batch data to the device
                    # so it matches location of the MODEL
                    x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                    # One step of training
                    yhat, loss = train_step(x_batch, y_batch)
                    tLoss1.append(loss)
                    tAcc1 += GetOneHotAccuracyValues(yhat, y_batch)

                with torch.no_grad():
                # Uses loader to fetch one mini-batch for validation
                    
                    for x_val, y_val in val_loader:
                        # Again, sends data to same device as model
                        x_val, y_val = x_val.to(device), y_val.to(device)
                        
                        # What is that?!
                        model.eval()
                        # Makes predictions
                        yhat = model(x_val)
                        #print(yhat)

                        # Computes validation loss and accuracy
                        val_loss = loss_fn(yhat, y_val)
                        vLoss1.append(val_loss)
                        vAcc1 += GetOneHotAccuracyValues(yhat, y_val)
                          
                    trLoss, vLoss = np.mean(tLoss1), np.mean(vLoss1)
                    trAcc, vAcc = GetAccValue(tAcc1), GetAccValue(vAcc1)

                    val_losses.append(vLoss)
                    tr_losses.append(trLoss)
                    val_accuracy.append(vAcc)
                    tr_accuracy.append(trAcc)

                    print("epoch ", epoch, " TrLoss = ", trLoss, " TAcc = ", trAcc, " Vloss = ", vLoss, " Vacc = ", vAcc)
            
            print("------------------- training losses ")
            PrintList(tr_losses, "../../raeResults/{}/learning/{}/TLoss.txt".format(resultsFolder, domain))

            print("------------------- validation losses")
            PrintList(val_losses, "../../raeResults/{}/learning/{}/VLoss.txt".format(resultsFolder, domain))
            
            #printList(val_losses)
            #CreatePlot(tr_losses, val_losses)
            #print(" mean training loss " , np.mean(tr_losses))
            #print(" mean validation loss ", np.mean(val_losses))

            print("------------------- Training accuracy")
            PrintList(tr_accuracy, "../../raeResults/{}/learning/{}/TAcc.txt".format(resultsFolder, domain))

            print("------------------- Validation accuracy")
            PrintList(val_accuracy, "../../raeResults/{}/learning/{}/Vacc.txt".format(resultsFolder, domain))

            torch.save(model.state_dict(), "models/{}/model_to_choose_{}_{}".format(resultsFolder, domain, modelFrom))
            


