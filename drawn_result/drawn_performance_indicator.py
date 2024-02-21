from utils.utils import cal_hv, cal_igd
import json
import numpy as np

def cal_hv_generation(file):
    with open(file, 'r') as f:
        # read json
        data = json.load(f)
    
    
    hv = []
    for key, value in data.items():
        gen = []
        for indi in value:
            gen.append([indi['obj1'], indi['obj2']])
        hv.append(cal_hv(np.array(gen), np.array([1, 1])))
    return hv


