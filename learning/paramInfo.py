nFeatures = {
    "EE": 182, #22,
    "SD": 126, #24,
    "SR": 330, #23,
    "OF": 0,
    "CR": 97, #22, #91
    }

params = {
    'SD': {
       'MoveThroughDoorway_Method2': 
            {'r2': {'nOutputs': 4, 'nInputs': 150}},
       'Recover_Method1': 
            {'r2': {'nOutputs': 4, 'nInputs': 128}},
    },
    'OF': {
        'Order_Method1': ['m', 'objList'],
        'Order_Method2': ['m', 'objList', 'p'],
        'PickupAndLoad_Method1': ['r'],
        'UnloadAndDeliver_Method1': ['r'],
        'MoveToPallet_Method1': ['r'], 
    },
}