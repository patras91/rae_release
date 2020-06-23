figuresFolder = "figures/"
#resultsFolder = "../../../raeResults/AIJ2020/"
resultsFolder = "../../../raeResults/SDN/"

ptMax = 247264 # maximum planning time

errIndex = {
        'nu': 'nu_error',
        'successRatio': 'sr_error',
        'retryRatio': 'rr_error',
        'totalTime': 'tt_error',
    }

B_max_depth = {
    "SD": [2,5,8],
    'EE': [1, 2, 3],
    'IP': [1, 2, 3],
    'CR': [1, 2, 3],
    'SR': [2, 3, 4],
    'OF': [3, 6, 9]
}

B_lim_depth = {
    'SD': [2,5,8],
    'EE': [1, 2, 3],
    'IP': [1, 2, 3],
    'CR': [1,2],
    'SR': [2, 3, 4],
    'OF': [3,6,9]
}

K_lim_depth = {
    'SD': 3,
    'EE': 3,
    'IP': 3,
    'CR': 3,
    'SR': 3,
}

K_max_depth = {
    "SD": [0, 1,3,5],
    'EE': [0, 1, 3, 5, 8, 10], #, 20, 50, 75, 100],
    'IP': [0, 3, 5, 7, 10],
    'CR': [0,1,3,5], #20, 30, 40, 50, 60, 70, 75, 80, 90, 100],
    'SR': [0, 1, 3, 5],
    'OF': [0, 1, 3, 5]
}

Depth = {
    'SR': [0, 1, 2, 5, 10, 15, 20], #25, 30], # 35, 40, 45, 50],
    'CR': [0, 1, 2, 5, 10, 15, 20], #25, 30], # 35, 40, 45, 50],
    'OF': [0, 1, 2, 5, 10, 15, 20], # 35, 40, 45, 50],
    'SD': [0, 1, 2, 5, 10, 15, 20], #25, 30], # 35, 40, 45, 50],
    'EE': [0, 1, 2, 5, 10, 15, 20], #25, 30], #35, 40, 50, 60],
}

#UCT_max_depth = {
#    'CR': [0, 5, 25, 50, 75, 100, 125],
#    'SR': [0, 5, 25, 50, 75, 100, 125],
#    'OF': [0, 5, 25, 50, 75, 100, 125, 150],
#    'SD': [0, 5, 25, 50, 75, 100, 125],
#    'EE': [0, 5, 25, 50, 75, 100, 125],
#}

UCT_max_depth = {
    "CR": [0, 5, 10, 25, 50, 100, 250], #, 500, 1000], # 2500, 5000],
    "SR": [0, 5, 10, 25, 50, 100, 250], # 2500],
    "SD": [0, 5, 10, 25, 50, 100, 250], #, 2500],
    "EE": [0, 5, 10, 25, 50, 100, 250], #, 2500, 5000],
    'OF': [0, 5, 10, 25, 50, 100, 250], #, 2500, 5000],
    'SDN': [0, 5, 25, 50, 100],
}

UCT_lim_depth = {
    "h0": {
    'CR': [1000],
    'SR': [1000],
    'OF': [1000],
    'SD': [1000],
    'EE': [1000],
    },
    "h1": {
    'CR': [1000],
    'SR': [1000],
    'OF': [1000],
    'SD': [1000],
    'EE': [1000],
    },
    "learnH": {
    'CR': [250],
    'SR': [250],
    'OF': [250],
    'SD': [250],
    'EE': [250],
    }
}

def Get_nro_in_lim_depth(h, d):
    if d <= 4 or h == "learnH":
        return 250
    else:
        return 1000

timeLimit = {
    "OF": 1800,
    "CR": 1800,
    "SR": 1800,
    "EE": 1800,
    "SD": 1800,
    "SDN": 300,
}


def GetFullName(domain):
    if domain == "CR":
        return "Fetch Domain"
    elif domain == "SD":
        return "Nav Domain"
        return "Navigate Doorways Domain"
    elif domain == "SR":
        return "S & R domain"
        return "Search and Rescue Domain"
    elif domain == "OF":
        return "Deliver Domain"
        return "Order Delivery Domain"
    elif domain == "EE":
        return "Explore Domain"
        return "Explore Environment Domain"
    elif domain == "SDN":
        return "Security Domain"

# The set of problems with 1 task, 2 tasks, and 3 tasks in each domain
problems_with_n_tasks = {
    'SD': {1: ['problem1119', 'problem1059', 'problem1029', 'problem1103', 'problem1121', 'problem1063', 'problem1057', 'problem1069', 'problem1055', 'problem1083', 'problem1049', 'problem1039', 'problem1125', 'problem1087', 'problem1115', 'problem1033', 'problem1019', 'problem1089', 'problem1053', 'problem1085', 'problem1051', 'problem1107', 'problem1045', 'problem1007', 'problem1003', 'problem1013', 'problem1127', 'problem1027', 'problem1043'], 2: ['problem1014', 'problem1070', 'problem1068', 'problem1106', 'problem1028', 'problem1046', 'problem1100', 'problem1086', 'problem1116', 'problem1124', 'problem1084', 'problem1066', 'problem1010', 'problem1078', 'problem1120', 'problem1110', 'problem1032', 'problem1104', 'problem1036', 'problem1016', 'problem1094'], 3: []},
    'EE': {1: ['problem187', 'problem91', 'problem159', 'problem131', 'problem7', 'problem35', 'problem3', 'problem31', 'problem103', 'problem75', 'problem123', 'problem143', 'problem163', 'problem43', 'problem183'], 2: ['problem5', 'problem108', 'problem72', 'problem85', 'problem173', 'problem44', 'problem29', 'problem20', 'problem129', 'problem188', 'problem161', 'problem17', 'problem89', 'problem136', 'problem104', 'problem57', 'problem52', 'problem156', 'problem168', 'problem164', 'problem68', 'problem73'], 3: ['problem170', 'problem134', 'problem190', 'problem86', 'problem58', 'problem158', 'problem78', 'problem42', 'problem14', 'problem50', 'problem2', 'problem174', 'problem178']},
    'CR': {
        1: ['problem1004', 'problem1002', 'problem1096', 'problem1073', 'problem1012', 'problem1005', 'problem1087', 'problem1069', 'problem1089', 'problem1001', 'problem1008', 'problem1013', 'problem1092', 'problem1079', 'problem1085', 'problem1011', 'problem1076', 'problem1036', 'problem1099', 'problem1038', 'problem1028', 'problem1088', 'problem1007', 'problem1017', 'problem1040', 'problem1074', 'problem1078', 'problem1009', 'problem1045', 'problem1032', 'problem1046', 'problem1027', 'problem1041', 'problem1019'], 
        2: ['problem1106', 'problem1114', 'problem1053', 'problem1062', 'problem1111', 'problem1110', 'problem1120', 'problem1100', 'problem1118', 'problem1056', 'problem1108', 'problem1061', 'problem1065', 'problem1112', 'problem1067', 'problem1066'], 
        3: [],
        },
    'SR': {1: ['problem43', 'problem32', 'problem102', 'problem96', 'problem73', 'problem105', 'problem27', 'problem85', 'problem35', 'problem36', 'problem38', 'problem24', 'problem89', 'problem75', 'problem76', 'problem106', 'problem108', 'problem78', 'problem88', 'problem39', 'problem95', 'problem72', 'problem46', 'problem107', 'problem92', 'problem21', 'problem110', 'problem71', 'problem30', 'problem113', 'problem60', 'problem64', 'problem42', 'problem84', 'problem23', 'problem97', 'problem111', 'problem90', 'problem65', 'problem54', 'problem56', 'problem112', 'problem98', 'problem109', 'problem55', 'problem81', 'problem100', 'problem50', 'problem104', 'problem74'], 2: [], 3: []},
    'OF': {
        1: ['problem55', 'problem109', 'problem72', 'problem53', 'problem45', 'problem73', 'problem89', 'problem51', 'problem74', 'problem11', 'problem39', 'problem68', 'problem56', 'problem95', 'problem77', 'problem66', 'problem97', 'problem42', 'problem64', 'problem61', 'problem13'], 
        2: ['problem12', 'problem25', 'problem48', 'problem57', 'problem103', 'problem20', 'problem37', 'problem21', 'problem36', 'problem29', 'problem76', 'problem105', 'problem15', 'problem67', 'problem90', 'problem27', 'problem18', 'problem34', 'problem23', 'problem91', 'problem28', 'problem22', 'problem59', 'problem47', 'problem30', 'problem78', 'problem49', 'problem75', 'problem94'], 
        3: []
    },
    'SDN': {
        1: ['problem1', 'problem2', 'problem3', 'problem4', 'problem5', 'problem6', 'problem7', 'problem8', 'problem9', 'problem10'],
        2: [],
        3: [],
    }
}

def GetNewDict():
    return {
            'successRatio': [], 
            'retryRatio': [],
            'planTime': [],
            'actTime': [],
            'totalTime': [],
            'nu': [],
            'timeOut': [],
            'nu_error': [],
            'sr_error': [],
            'rr_error': [],
            'tt_error': [],
            }

def GetRAEfname(domain):
    return "{}{}_v_journal/RAE.txt".format(resultsFolder, domain)

def GetLowerLim(domain):
    if domain == "SR":
        return 0.8
    elif domain == "SDN":
        return 0
    else:
        return 0.9

COLORS = ['ro:', 'bs--', 'm^-.', 'go--', 'c^:', 'rs--', 'ms--', 'gs--']

COLORBAR = ['orange', 'grey', 'black',  'turquoise', 'orchid', 'orangered', 'yellowgreen', ]

