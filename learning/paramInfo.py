def DecodeRobot_SD(r):
    return {
        0: "r1",
        1: "r2",
        2: "r3",
        3: "r4",
    }[r]

def DecodeRobot_OF(r):
    return {
        0: "r0",
        1: "r1",
        2: "r2",
        3: "r3",
        4: "r4",
        5: "r5",
        6: "r6",
    }[r]

def DecodeMachine_OF(m):
    return {
        0: "m0",
        1: "m1",
        2: "m2",
        3: "m3",
        4: "m4",
    }[m]

def DecodePalate_OF(p):
    return {
        0: "p0",
        1: "p1",
        2: "p2",
        3: "p3",
    }[p]

def DecodeObjList_OF(o):
    return {
        0: ('o1',),
        1: ('o1',),
        2: ('o2',),
        3: ('o3',),
        4: ('o4',),
        5: ('o5',),
        6: ('o6',),
        7: ('o7',),
        8: ('o8',),
        9: ('o9',),
    }[o]

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
            {'r2': {'nOutputs': 4, 'nInputs': 150, 'pos': -1, 'decoder': DecodeRobot_SD}},
       'Recover_Method1': 
            {'r2': {'nOutputs': 4, 'nInputs': 128, 'pos': -1, 'decoder': DecodeRobot_SD}},
    },
    'OF': {
        'Order_Method1':  {
            'm': {'nOutputs': 5, 'nInputs': 613, 'pos': -2, 'decoder': DecodeMachine_OF}, 
            'objList': {'nOutputs': 10, 'nInputs': 613, 'pos': -1, 'decoder': DecodeObjList_OF},
            },
        'Order_Method2': {
            'm': {'nOutputs': 5, 'nInputs': 613, 'pos': -3, 'decoder': DecodeMachine_OF}, 
            'objList': {'nOutputs': 10, 'nInputs': 613, 'pos': -2, 'decoder': DecodeObjList_OF}, 
            'p': {'nOutputs': 4, 'nInputs': 613, 'pos': -1,  'decoder': DecodePalate_OF},
            },
        'PickupAndLoad_Method1': 
            {'r': {'nOutputs': 7, 'nInputs': 637, 'pos': -1, 'decoder': DecodeRobot_OF}},
        'UnloadAndDeliver_Method1': 
            {'r': {'nOutputs': 7, 'nInputs': 625, 'pos': -1, 'decoder': DecodeRobot_OF}},
        'MoveToPallet_Method1': 
            {'r': {'nOutputs': 7, 'nInputs': 633, 'pos': -1, 'decoder': DecodeRobot_OF}}, 
    },
}