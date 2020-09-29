import random


# Define some constants

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

min_num_ctrls = 1
max_num_ctrls = 4

min_num_switches = 16
max_num_switches = 64

normal_health_min = 40
normal_health_max = 100
weak_health_min = 0
weak_health_max = 48

normal_cpu_min = 10
normal_cpu_max = 100
weak_cpu_min = 91
weak_cpu_max = 150

normal_hosts_min = 32
normal_hosts_max = 11000
weak_hosts_min = 10001
weak_hosts_max = 20000

normal_flows_min = 16
normal_flows_max = 1000
weak_flows_min = 801
weak_flows_max = 1200


def GetWeakComponent(nCtrl, nSwitches):
    # Assign low health, no matter the component type
    v1 = random.randint(weak_health_min, weak_health_max)/100
    # For now, assign normal CPU (applies to both component types)
    v2 = random.randint(normal_cpu_min, normal_cpu_max)
    type = random.choice(["CTRL", "SWITCH"])
    if type == "CTRL":
        id = "ctrl" + str(random.randint(1, nCtrl))
        v3 = random.randint(normal_hosts_min, normal_hosts_max)
        # Assign one or more abnormal symptoms
        params = random.choice(["CPU", "HOSTS", "BOTH"])
        if params == "CPU":
            v2 = random.randint(weak_cpu_min, weak_cpu_max)
        elif params == "HOSTS":
            v3 = random.randint(weak_hosts_min, weak_hosts_max)
        elif params == "BOTH":
            # Further penalize health
            v1 = v1/2
            v2 = random.randint(weak_cpu_min, weak_cpu_max)
            v3 = random.randint(weak_hosts_min, weak_hosts_max)
    else:
        id = "switch" + str(random.randint(1, nSwitches))
        v3 = random.randint(normal_flows_min, normal_flows_max)
        # Assign one or more abnormal symptoms
        params = random.choice(["CPU", "FLOWS", "BOTH"])
        if params == "CPU":
            v2 = random.randint(weak_cpu_min, weak_cpu_max)
        elif params == "FLOWS":
            v3 = random.randint(weak_flows_min, weak_flows_max)
        elif params == "BOTH":
            # Further penalize health
            v1 = v1/2
            v2 = random.randint(weak_cpu_min, weak_cpu_max)
            v3 = random.randint(weak_flows_min, weak_flows_max)

    return id, (v1, v2, v3)


def WriteComponent(file, id, type, is_crit):
    file.write("        \'{}\': ".format(id) + "{\n")
    file.write("            \'id\': \'{}\',\n".format(id))
    file.write("            \'type\': \'{}\',\n".format(type))
    file.write("            \'critical\': {}\n".format(is_crit))
    file.write("        },\n")


def WriteComponentStat(file, id, type, v1, v2, v3):
    file.write("        \'{}\': ".format(id) + "{\n")
    file.write("            \'health\': {\n")
    file.write("                \'value\': {},\n".format(v1))
    file.write("                \'thresh_exceeded_fn\': health_exceeded_fn\n")
    file.write("            },\n")
    file.write("            \'cpu_perc_ewma\': {\n")
    file.write("                \'value\': {},\n".format(v2))
    file.write("                \'thresh_exceeded_fn\': cpu_perc_exceeded_fn\n")
    file.write("            },\n")
    if type == "CTRL":
        file.write("            \'host_table_size\': {\n")
        file.write("                \'value\': {},\n".format(v3))
        file.write("                \'thresh_exceeded_fn\': host_table_exceeded_fn\n")
    else:
        file.write("            \'flow_table_size\': {\n")
        file.write("                \'value\': {},\n".format(v3))
        file.write("                \'thresh_exceeded_fn\': flow_table_exceeded_fn\n")
    file.write("            }\n")
    file.write("        },\n")


def generateProblems():
    num = 1
    for i in range(100):
        writeProblem(num)
        num += 1


def writeProblem(num):
    fname = 'auto/problem{}_SDN.py'.format(num)
    file = open(fname, "w")
    writeHeader(file)

    nCntr = random.randint(min_num_ctrls, max_num_ctrls)
    nSwitches = random.randint(min_num_switches, max_num_switches)

    file.write("def ResetState():\n\n")
    file.write("    state.components = {\n")

    for i in range(1, nCntr + 1):
        id = "ctrl{}".format(i)
        is_crit = random.choice([True, False])
        WriteComponent(file, id, "CTRL", is_crit)

    for i in range(1, nSwitches + 1):
        id = "switch{}".format(i)
        is_crit = random.choice([True, False])
        WriteComponent(file, id, "SWITCH", is_crit)

    file.write("    }\n\n")

    weakComp, value = GetWeakComponent(nCntr, nSwitches)

    file.write("    state.stats = {\n")

    weak_ids = []
    for i in range(1, nCntr + 1):
        id = "ctrl{}".format(i)
        if id == weakComp:
            v1, v2, v3 = value
            weak_ids.append(id)
        else:
            v1 = random.randint(normal_health_min, normal_health_max)/100
            v2 = random.randint(normal_cpu_min, normal_cpu_max)
            v3 = random.randint(normal_hosts_min, normal_hosts_max)
            if v1 < secmgr_config['health_action_thresh']:
                weak_ids.append(id)
        WriteComponentStat(file, id, "CTRL", v1, v2, v3)

    for i in range(1, nSwitches + 1):
        id = "switch{}".format(i)
        if id == weakComp:
            v1, v2, v3 = value
            weak_ids.append(id)
        else:
            v1 = random.randint(normal_health_min, normal_health_max)/100
            v2 = random.randint(normal_cpu_min, normal_cpu_max)
            v3 = random.randint(normal_flows_min, normal_flows_max)
            if v1 < secmgr_config['health_action_thresh']:
                weak_ids.append(id)
        WriteComponentStat(file, id, "SWITCH", v1, v2, v3)

    file.write("    }\n\n\n")

    file.write("rv.x = []\n\n")

    task_type = random.choice(["HANDLE_EVENT", "FIX_ONE", "FIX_MULT"])
    if task_type == "HANDLE_EVENT":
        file.write("event1 = {\n")
        file.write("    \'source\': \'sysmon\',\n")
        file.write("    \'type\': \'alarm\',\n")
        file.write("    \'component_id\': \'{}\'\n".format(weakComp))
        file.write("}\n\n")
        file.write("context = 'A security event was detected on {}'\n".format(weakComp))
        file.write("tasks = {\n")
        file.write("    1: [[\'handle_event\', event1, secmgr_config, context]]\n")
        file.write("}\n\n")
    elif task_type == "FIX_ONE":
        file.write("context = 'The component {} is low on resources'\n".format(weakComp))
        file.write("tasks = {\n")
        file.write("    1: [[\'fix_component\', \'{}\', secmgr_config, context]]\n".format(weakComp))
        file.write("}\n\n")
    elif task_type == "FIX_MULT":
        context = 'A number of components are low on resources, including {}'
        if len(weak_ids) < 2:
            context = 'The component {} is low on resources'
        file.write("tasks = {\n")
        cur_idx = 1
        for id in weak_ids:
            if cur_idx > 1:
                file.write(",\n")
            file.write("    {}: [[\'fix_component\', \'{}\', secmgr_config, \'{}\']]".format(
                cur_idx, id, context.format(id)
            ))
            cur_idx += 1
        file.write("\n}\n\n")

    file.write("eventsEnv = {")
    file.write("}\n")

    file.close()


def writeHeader(file):
    file.write("__author__ = 'patras'\n\n")
    file.write("import functools\n")
    file.write("import operator\n")
    file.write("from domain_AIRS import *\n")
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
    file.write(")\n\n\n")


if __name__ == "__main__":
    generateProblems()
