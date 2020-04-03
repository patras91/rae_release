figuresFolder = "figures/"
resultsFolder = "../../../raeResults/AIJ2020/"

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
    'SR': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    'CR': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    'OF': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    'SD': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    'EE': [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60],
}

#UCT_max_depth = {
#    'CR': [0, 5, 25, 50, 75, 100, 125],
#    'SR': [0, 5, 25, 50, 75, 100, 125],
#    'OF': [0, 5, 25, 50, 75, 100, 125, 150],
#    'SD': [0, 5, 25, 50, 75, 100, 125],
#    'EE': [0, 5, 25, 50, 75, 100, 125],
#}

UCT_max_depth = {
    "CR": [0, 50, 100, 250, 500, 1000], # 2500, 5000],
    "SR": [0, 50, 100, 250, 500, 1000], # 2500],
    "SD": [0, 50, 100, 250, 500, 1000], #, 2500],
    "EE": [0, 50, 100, 250, 500, 1000], #, 2500, 5000],
    'OF': [0, 50, 100, 250, 500, 1000], #, 2500, 5000],
}

UCT_lim_depth = {
    'CR': [1000],
    'SR': [1000],
    'OF': [1000],
    'SD': [1000],
    'EE': [1000],
}
