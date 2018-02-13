__author__ = 'patras'

from ete3 import Tree

y_old = ''
while(True):
    f = open('pipefile', 'r')
    y = f.read()
    f.close()
    if y != '' and y != y_old:
        t = Tree(y)
        t.show()
        t.close()
    y_old = y