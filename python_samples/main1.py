__author__ = 'patras'

import pipes

#while(True):
t = pipes.Template()
while (True):
    text = input("Any text:")
    f = t.open('pipefile', 'w')
    f.write(text)
    f.close()
    #f.write('are you there?')
#f.close()
    #