b_max_depth = {
    "CR": [1,2,3],
    "SD": [2,3,4],
    "SR": [2,3,4],
    "EE": [1,2,3],
    "IP": [1,2,3],
    "OF": [3,6,9],
}

k_max_depth = {
    "CR": [1,3,5],
    "SD": [],
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

UCT_max_depth = {
    "CR": [5, 25, 50, 75],
    "SD": [],
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

b_lim_depth = {
    "CR": [1,2],
    "SD": [2,3,4],
    "SR": [2,3,4],
    "EE": [1,2,3],
    "IP": [1,2,3],
    "OF": [3,6,9],
}

k_lim_depth = {
    "CR": [3],
    "SD": [],
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

UCT_lim_depth = {
    "CR": [5, 25, 50],
    "SD": [],
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

DEPTH = {
    "CR": [5, 10, 15],
    "SD": [5, 10, 15],
    "SR": [5, 10, 15],
    "EE": [5, 10, 15],
    "IP": [5, 10, 15],
    "OF": [5, 10, 15],
}

def MergeHelper(l, name):
    fwrite = open(name, "w")
    for f in l:
        fread = open(f, "r")
        content = fread.read()
        fwrite.write(content)

def Merge(domain, mode, depth):
    if mode == "SLATE" and depth == "max":
        for b in b_max_depth[domain]:
            for k in k_max_depth[domain]:
                fList = []
                for parts in range(1, 11):
                    name = "rae_plan_b_{}_k_{}_part_{}.txt".format(b,k,parts)
                    fList.append(name)
                fName = "rae_plan_b_{}_k_{}.txt".format(b,k)
                MergeHelper(fList, fName)

    elif mode == "SLATE" and depth == "lim":
        for b in b_lim_depth[domain]:
            for k in k_lim_depth[domain]:
                for d in DEPTH[domain]:
                    fList = []
                    for parts in range(1, 11):
                        name = "rae_plan_b_{}_k_{}_d_{}_part_{}.txt".format(b,k,d,parts)
                        fList.append(name)
                    fName = "rae_plan_b_{}_k_{}_d_{}.txt".format(b,k,d)
                    MergeHelper(fList, fName)

    elif mode == "UCT" and depth == "max":
        for uct in UCT_max_depth[domain]:
            fList = []
            for parts in range(1, 11):
                name = "rae_plan_uct_{}_part_{}.txt".format(uct,parts)
                fList.append(name)
            fName = "rae_plan_uct_{}.txt".format(uct)
            MergeHelper(fList, fName)

    else:
        for uct in UCT_lim_depth[domain]:
            for d in DEPTH[domain]:
                fList = []
                for parts in range(1, 11):
                    name = "rae_plan_uct_{}_d_{}_part_{}.txt".format(uct,d,parts)
                    fList.append(name)
                fName = "rae_plan_uct_{}_d_{}.txt".format(uct,d)
                MergeHelper(fList, fName)

if __name__ == "__main__":
    for domain in ["CR"]:
        for mode in ["SLATE", "UCT"]:
            for depth in ["max", "lim"]:
                Merge(domain, mode, depth)