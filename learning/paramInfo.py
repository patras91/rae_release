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
        'Order_Method1':  {
            'm': {'nOutputs': 5, 'nInputs': 613}, 
            'objList': {'nOutputs': 10, 'nInputs': 613},
            },
        'Order_Method2': {
            'm': {'nOutputs': 5, 'nInputs': 613}, 
            'objList': {'nOutputs': 10, 'nInputs': 613}, 
            'p': {'nOutputs': 4, 'nInputs': 613},
            },
        'PickupAndLoad_Method1': 
            {'r': {'nOutputs': 7, 'nInputs': 637}},
        'UnloadAndDeliver_Method1': 
            {'r': {'nOutputs': 7, 'nInputs': 625}},
        'MoveToPallet_Method1': 
            {'r': {'nOutputs': 7, 'nInputs': 633}}, 
    },
}