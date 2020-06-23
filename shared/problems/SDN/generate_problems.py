import random
import math


secmgr_config = {
    'health_warning_thresh': 0.6,
    'health_critical_thresh': 0.5,
    'health_action_thresh': 0.49,
    'cpu_ewma_alpha': 0.5,
    'cpu_perc_warning_thresh': 75,
    'cpu_perc_critical_thresh': 90,
    'host_table_critical_thresh': 10000,
    'flow_table_critical_thresh': 800
}

def GetWeakComponent(nCtrl, nSwitches):
    type = random.choice(["CTRL", "SWITCH"])
    if type == "CTRL":
        id = "ctrl" + str(random.randint(0,nCtrl))
        param = random.choice(["health", "cpu_perc", "host_table"])
        v1 = 1 # can also assign these randomly in the safe range
        v2 = 50
        v3 = 5000
        # assign the unsafe value randomly
        if param == "health":
            v1 = random.randint(1, 48)/100
        elif param == "cpu_perc":
            v2 = random.randint(91, 150)
        elif param == "host_table":
            v3 = random.randint(10001, 15000)

    else:
        id = "switch" + str(random.randint(0,nSwitches))
        param = random.choice(["health", "cpu_perc", "flow_table"])
        v1 = 1 # can also assign these randomly in the safe range
        v2 = 50
        v3 = 500
        # assign the unsafe value randomly
        if param == "health":
            v1 = random.randint(1, 48)/100
        elif param == "cpu_perc":
            v2 = random.randint(91, 150)
        elif param == "flow_table":
            v3 = random.randint(801, 1000)

    return id, (v1, v2, v3)

def WriteComponent(file, id, type, c):
    file.write("\'{}\': ".format(id) + "{\n")
    file.write("    \'id\': \'{}\',\n".format(id))
    file.write("    \'type\': \'{}\',\n".format(type))
    file.write("    \'critical\': {}\n".format(c))
    file.write("    },\n")

def WriteComponentStat(file, id, type, v1, v2, v3):
    file.write("\'{}\': ".format(id) + "{\n")
    file.write("        \'health\': {\n")
    file.write("            \'value\': {},\n".format(v1))
    file.write("            \'thresh_exceeded_fn\': health_exceeded_fn\n")
    file.write("        },\n")
    file.write("        \'cpu_perc_ewma\': {\n")
    file.write("            \'value\': {},\n".format(v2))
    file.write("            \'thresh_exceeded_fn\': cpu_perc_exceeded_fn\n")
    file.write("        },\n")
    if type == "CTRL":
        file.write("        \'host_table_size\': {\n")
        file.write("            \'value\': {},\n".format(v3))
        file.write("            \'thresh_exceeded_fn\': host_table_exceeded_fn\n")
    else:
        file.write("        \'flow_table_size\': {\n")
        file.write("            \'value\': {},\n".format(v3))
        file.write("            \'thresh_exceeded_fn\': flow_table_exceeded_fn\n")
    file.write("        }\n")
    file.write("    },\n")

def generateProblems():
    num = 1
    for i in range(100):
        writeProblem(num)
        num += 1

def writeProblem(num):
    fname = 'auto/problem{}_SDN.py'.format(num)
    file = open(fname,"w") 
    writeHeader(file)

    nCntr = random.randint(4,15)
    nSwitches = random.randint(5, 20)

    file.write("def ResetState():\n\n")
    file.write("    state.components = {\n")

    for i in range(nCntr):
        id = "ctrl{}".format(i)
        c = random.choice([True, False])
        WriteComponent(file, id, "CTRL", c)

    for i in range(nSwitches):
        id = "switch{}".format(i)
        c = random.choice([True, False])
        WriteComponent(file, id, "SWITCH", c)

    file.write("    }\n\n")

    weakComp, value = GetWeakComponent(nCntr, nSwitches)

    file.write("    state.stats = {\n")

    for i in range(nCntr):
        id = "ctrl{}".format(i)
        if id == weakComp:
            v1, v2, v3 = value
        else:
            v1 = random.randint(1, 100)/100
            v2 = random.randint(25,120)
            v3 = random.randint(5000, 15000)
        WriteComponentStat(file, id, "CTRL", v1, v2, v3)

    for i in range(nSwitches):
        id = "switch{}".format(i)
        if id == weakComp:
            v1, v2, v3 = value
        else:
            v1 = random.randint(1, 100)/100
            v2 = random.randint(25,120)
            v3 = random.randint(200,1500)
        WriteComponentStat(file, id, "SWITCH", v1, v2, v3)

    file.write("    }\n\n")

    file.write("rv.x = []\n\n")
    
    file.write("event1 = {\n")
    file.write("    \'source\': \'sysmon\',\n")
    file.write("    \'type\': \'alarm\',\n")
    file.write("    \'component_id\': \'{}\'\n".format(weakComp))
    file.write("}\n\n")

    file.write("tasks = {\n")
    file.write("    1: [[\'handle_event\', event1, secmgr_config]]\n")
    file.write("}\n\n")

    file.write("eventsEnv = {")
    file.write("}\n\n")

    file.close() 

def writeHeader(file):
    file.write("__author__ = 'patras'\n\n")
    file.write("import functools\n")
    file.write("import operator\n")
    file.write("from domain_AIRS import *\n") 
    file.write("from timer import DURATION\n") 
    file.write("from state import state\n\n")


    file.write("secmgr_config = {\n")
    file.write("    \'health_warning_thresh\': 0.6,\n")
    file.write("    \'health_critical_thresh\': 0.5,\n")
    file.write("    \'health_action_thresh\': 0.49,\n")
    file.write("    \'cpu_ewma_alpha\': 0.5,\n")
    file.write("    \'cpu_perc_warning_thresh\': 75,\n")
    file.write("    \'cpu_perc_critical_thresh\': 90,\n")
    file.write("    \'host_table_critical_thresh\': 10000,\n")
    file.write("    \'flow_table_critical_thresh\': 800\n")
    file.write("}\n\n")

    file.write("health_exceeded_fn = functools.partial(\n")
    file.write("    operator.ge,\n")
    file.write("    secmgr_config[\'health_action_thresh\']\n")
    file.write(")\n\n")

    file.write("cpu_perc_exceeded_fn = functools.partial(\n")
    file.write("    operator.le,\n")
    file.write("    secmgr_config[\'cpu_perc_critical_thresh\']\n")
    file.write(")\n\n")

    file.write("host_table_exceeded_fn = functools.partial(\n")
    file.write("    operator.le,\n")
    file.write("    secmgr_config[\'host_table_critical_thresh\']\n")
    file.write(")\n\n")

    file.write("flow_table_exceeded_fn = functools.partial(\n")
    file.write("    operator.le,\n")
    file.write("    secmgr_config[\'flow_table_critical_thresh\']\n")
    file.write(")\n\n")
 

if __name__=="__main__":
    generateProblems()