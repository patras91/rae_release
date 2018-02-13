__author__ = 'patras'

from ete3 import Tree

def DrawTree():
    y_old = ''
    count = 0
    while(True):
        f = open('pipefile', 'r')
        y = f.read()
        f.close()
        if y != '' and y != y_old:
            t = Tree(y)
            t.render("figures/RTree_{}.png".format(count))
            count += 1
        y_old = y

if __name__=="__main__":
    DrawTree()