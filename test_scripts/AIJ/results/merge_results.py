b_max_depth = {
    "CR": [1,2,3],
    "SD": [2,5,8],
    "SR": [2,3,4],
    "EE": [1,2,3],
    "IP": [1,2,3],
    "OF": [3,6,9],
}

k_max_depth = {
    "CR": [1,3,5],
    "SD": [1,3,5],
    "SR": [1,3,5],
    "EE": [],
    "IP": [],
    "OF": [1,3,5],
}

UCT_max_depth = {
    "CR": [5, 25, 50, 75],
    "SD": [5, 25, 50, 75],
    "SR": [5, 25, 50, 75],
    "EE": [],
    "IP": [],
    "OF": [5, 25, 50, 75],
}

b_lim_depth = {
    "CR": [1,2],
    "SD": [2,5,8],
    "SR": [2,3,4],
    "EE": [1,2,3],
    "IP": [1,2,3],
    "OF": [3,6,9],
}

k_lim_depth = {
    "CR": [3],
    "SD": [3],
    "SR": [3],
    "EE": [],
    "IP": [],
    "OF": [3],
}

UCT_lim_depth = {
    "CR": [5, 25, 50],
    "SD": [5, 25, 50],
    "SR": [5, 25, 50],
    "EE": [],
    "IP": [],
    "OF": [5, 25, 50],
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
                    name = "{}_v_journal/rae_plan_b_{}_k_{}_part_{}.txt".format(domain, b,k,parts)
                    fList.append(name)
                fName = "{}_v_journal/rae_plan_b_{}_k_{}.txt".format(domain, b,k)
                MergeHelper(fList, fName)

    elif mode == "SLATE" and depth == "lim":
        for b in b_lim_depth[domain]:
            for k in k_lim_depth[domain]:
                for d in DEPTH[domain]:
                    fList = []
                    for parts in range(1, 11):
                        name = "{}_v_journal/rae_plan_b_{}_k_{}_d_{}_part_{}.txt".format(domain, b,k,d,parts)
                        fList.append(name)
                    fName = "{}_v_journal/rae_plan_b_{}_k_{}_d_{}.txt".format(domain, b,k,d)
                    MergeHelper(fList, fName)

    elif mode == "UCT" and depth == "max":
        for uct in UCT_max_depth[domain]:
            fList = []
            for parts in range(1, 11):
                name = "{}_v_journal/rae_plan_uct_{}_part_{}.txt".format(domain, uct,parts)
                fList.append(name)
            fName = "{}_v_journal/rae_plan_uct_{}.txt".format(domain, uct)
            MergeHelper(fList, fName)

    else:
        for uct in UCT_lim_depth[domain]:
            for d in DEPTH[domain]:
                fList = []
                for parts in range(1, 11):
                    name = "{}_v_journal/rae_plan_uct_{}_d_{}_part_{}.txt".format(domain, uct,d,parts)
                    fList.append(name)
                fName = "{}_v_journal/rae_plan_uct_{}_d_{}.txt".format(domain, uct,d)
                MergeHelper(fList, fName)

if __name__ == "__main__":
    for domain in ["SD"]:
        for mode in ["UCT"]:
            for depth in ["max", "lim"]:
                Merge(domain, mode, depth)