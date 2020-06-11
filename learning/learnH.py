import torch
import numpy as np 
from torch.utils.data import Dataset, TensorDataset, DataLoader
from torch.utils.data.dataset import random_split
import torch.nn as nn
import torch.optim as optim
import argparse
import pdb
import random
from torch.optim.lr_scheduler import MultiStepLR

device = 'cpu' #if torch.cuda.is_available() else 'cpu'
domain = None
modelFrom = None
folderPrefix = "../../raeResults/AIJ2020/learning/"

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

        #print("y =  ,", y)
        #print("yhat = ", yhat) 

        #print("in training yhat = ", yhat)
        #print("in training y = ", y)

        loss = 1 * loss_fn(yhat, y)
        # Computes gradients
        loss.backward()
        # Updates parameters and zeroes gradients
        optimizer.step()
        optimizer.zero_grad()
        # Returns the loss
        return loss.item(), yhat
    
    # Returns the function that will be called inside the train loop
    return train_step

# Builds a simple sequential model

features = {
    "EE": 204, #23 - 2,
    "SD": 144, #25 - 2,
    "SR": 401, #24 - 2,
    "OF": 627,
    "CR": 100, #23 - 2,
}

outClasses = {
    "EE": 200,
    "SD": 75,
    "SR": 10,
    "OF": 10, #150,
    "CR": 100, #1
}

n_epochs = 10

# Defines loss function and optimizer
#loss_fn = nn.MSELoss(reduction='mean')
#loss_fn = nn.SmoothL1Loss(reduction='sum')
loss_fn = nn.CrossEntropyLoss()
#loss_fn = nn.CrossEntropyLoss()
#loss_fn = nn.NLLLoss()
#loss_fn = nn.BCEWithLogitsLoss()


tr_losses = []
val_losses = []
tr_accuracy = []
val_accuracy = []

def GetLabel(yhat):
    r, predicted = torch.max(yhat, 0)
    return predicted.long()

def GetAccValue(acc):
    v = 0
    s = 0
    for i in acc:
        v += i
        s += 1
    return v/s

def GetOneHotAccuracyValues(yhat, y):
    res = []
    for i1, i2 in zip(yhat, y):
        l = GetLabel(i1)
        if l == i2:
            res.append(1)
        else:
            res.append(0)
    return res

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
        "OF": 10,
    }
    x = list(range(0, len(training)))

    #print("x is ", x)
    #print("training is, ", training)
    PlotViaMatlab(x,
                training,
                COLORS[0],
                'Training Loss in {} domain'.format(domain))
    PlotViaMatlab(list(range(0, len(validation))),
                validation,
                COLORS[1],
                'Validation Loss in {} domain'.format(domain))

    fname = 'Loss_eff_{}_{}.png'.format(domain, modelFrom)
    plt.xlabel('Training steps')
    plt.xticks(np.arange(min(x), max(x)+10, gap[domain]))
    plt.ylabel("Loss")
    plt.legend(bbox_to_anchor=(0.3, 1), loc=3, ncol=1, borderaxespad=0.)
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
    argparser.add_argument("--task", help="which task? ('all' for all together)",
                           type=str, required=True)

    args = argparser.parse_args()
    domain = args.domain
    n_epochs = args.nepochs

    if args.modelFrom == 'a':
        modelFrom = "actor"
    else:
        modelFrom = "planner"

    if args.task == "all":
        fileIn = open("{}{}/numericData_eff_{}_{}.txt".format(folderPrefix, domain, domain, modelFrom))
    else:
        fileIn = open("{}{}/numericData_eff_{}_{}_task_{}.txt".format(folderPrefix, domain, domain, modelFrom, args.task))
    
    x = []
    y = []
    line = fileIn.readline()

    r = np.random.rand()
    while(line != ""):
        nums = line[0:-1]
        if r < 2:
            items = nums.split(" ")
            x_row = [float(i) for i in items[0:-1]]
            while(len(x_row) < features[domain]):
                x_row.append(0)
            x.append(x_row)
            
            y_row = int(items[-1]) + 1
            #if y_row > 90:
            #    print(y_row)
            y.append(y_row)
        r = np.random.rand()
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

    x = np.array(x)
    y = np.array(y)

    #x = np.random.rand(10, 3, 1)
    #print(" x is ", x)
    #y = 1 + .1 * np.random.randn(10, 1)
    print(x.dtype)
    x_tensor = torch.from_numpy(x).float()
    y_tensor = torch.from_numpy(y).long()

    # Builds dataset with ALL data
    dataset = TensorDataset(x_tensor, y_tensor)
    # Splits randomly into train and validation datasets
    train_dataset, val_dataset = random_split(dataset, [trainingSetSize[domain], validationSetSize[domain]]) 
    # Builds a loader for each dataset to perform mini-batch gradient descent
    train_loader = DataLoader(dataset=train_dataset, batch_size=128)
    val_loader = DataLoader(dataset=val_dataset, batch_size=128)

    #model = nn.Sequential(nn.Linear(features[domain], 1)).to(device) 
    if domain == "EE" or domain == "SR" or domain == "SD" or domain == "CR" or domain == "OF":
        model = nn.Sequential(nn.Linear(features[domain], 512), 
            nn.ReLU(inplace=True),
            #nn.Linear(1024, 1024), 
            #nn.ReLU(inplace=True),
            #nn.Tanh(),
            #nn.Tanhshrink(),
            #nn.Softplus(),
            #nn.Sigmoid(), 
            #nn.Dropout(p=0.1), 
            #nn.PReLU(),
            #nn.Sigmoid(),
            #nn.Linear(512, 512), 
            #nn.ReLU(inplace=True), 
            nn.Linear(512, outClasses[domain]))
            #nn.Sigmoid()))
    elif domain == "CR":
        model = nn.Sequential(nn.Linear(features[domain], 512), 
            nn.ReLU(inplace=True),
            nn.Linear(512, 512), 
            nn.Dropout(p=0.1),
            nn.Linear(512, 512), 
            nn.ReLU(inplace=True), 
            nn.Linear(512, outClasses[domain]))
    #print(model.state_dict())

    # Sets hyper-parameters
    if modelFrom == "actor":
        lrD = {
            "EE": 1e-3,
            "SD": 1e-3,
            "SR": 1e-3,
            "CR": 1e-2,
            "OF": 1e-3,
        }
    else:
        lrD = {
            "EE": 1e-1,
            "SD": 1e-1,
            "SR": 1e-1,
            "CR": 1e-1,
            "OF": 1e-2,
        }
    lr = lrD[domain]

    optimizer = optim.SGD(model.parameters(), lr=lr)

    # Creates function to perform train step from model, loss and optimizer
    train_step = make_train_step(model, loss_fn, optimizer)

    #scheduler = MultiStepLR(optimizer, milestones=[30, 60], gamma=0.9) 

    # Training loop
    for epoch in range(n_epochs):
        # Uses loader to fetch one mini-batch for training
        
        #scheduler.step()
        tAcc1 = []
        tLoss1 = []
        for x_batch, y_batch in train_loader:

            # NOW, sends the mini-batch data to the device
            # so it matches location of the MODEL

            x_batch = x_batch.to(device)
            #pdb.set_trace()
            y_batch = y_batch.to(device)
            # One step of training
            loss, yhat = train_step(x_batch, y_batch)
            
            tLoss1.append(loss)
            tAcc1 += GetOneHotAccuracyValues(yhat, y_batch)

        with torch.no_grad():
        # Uses loader to fetch one mini-batch for validation
            vLoss1 = []

            vAcc1 = []


            for x_val, y_val in val_loader:
                # Again, sends data to same device as model
                x_val = x_val.to(device)
                y_val = y_val.to(device)
                
                # What is that?!
                model.eval()
                # Makes predictions
                yhat = model(x_val)
                #print(yhat)

                # Computes validation loss and accuracy
                #print("yhat is ", yhat)
                #print("yval is ", y_val)
                val_loss = loss_fn(yhat, y_val)
                vLoss1.append(val_loss)

                vAcc1 += GetOneHotAccuracyValues(yhat, y_val)
                #print("predicted", yhat)
                #print("real ", y_val)

            #for x_tr, y_tr in train_loader:
                # Again, sends data to same device as model
            #    x_tr = x_tr.to(device)
            #    y_tr = y_tr.to(device)
                
                # What is that?!
            #    model.eval()
                # Makes predictions
            #    yhat = model(x_tr)
            #    t_loss = loss_fn(yhat, y_tr)
            #    tLoss1.append(t_loss)
                
            #    tAcc1 += GetOneHotAccuracyValues(yhat, y_tr)

            num1 = np.mean(vLoss1)
            num2 = np.mean(tLoss1)
            num3 = GetAccValue(vAcc1)
            num4 = GetAccValue(tAcc1)
            val_losses.append(num1)
            tr_losses.append(num2)
            val_accuracy.append(num3)
            tr_accuracy.append(num4)
            print("epoch ", epoch, 
                " TLoss = ", num2, 
                " TAcc = ", num4, 
                " VLoss = ", num1, 
                " VAcc = ", num3)
        
    print("------------------- training losses ")
    PrintList(tr_losses, "{}{}/TLoss_eff.txt".format(folderPrefix, domain))

    print("------------------- validation losses")
    PrintList(val_losses, "{}{}/VLoss_eff.txt".format(folderPrefix, domain))

    #CreatePlot(tr_losses, val_losses)
    #print(" mean training loss " , np.mean(tr_losses))
    #print(" mean validation loss ", np.mean(val_losses))

    print("------------------- Training accuracy")
    PrintList(tr_accuracy, "{}{}/TAcc_eff.txt".format(folderPrefix, domain))

    print("------------------- Validation accuracy")
    PrintList(val_accuracy, "{}{}/Vacc_eff.txt".format(folderPrefix, domain))

    torch.save(model.state_dict(), "models/AIJ2020/model_for_eff_{}_{}_task_{}".format(domain, modelFrom, args.task))
    


