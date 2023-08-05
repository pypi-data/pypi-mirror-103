import sys

import matplotlib.pyplot as plt
from jjy.framework.functions import *
import matplotlib.pyplot as plt
from jjy.framework.functions import *
from PIL import Image
import os
#
import jjy.framework.layer as Layer
import jjy.framework.optimizer as Optimizer
import jjy.framework.initializer as Initializer
from jjy.framework.functions import *
from jjy.framework.network import MultiLayerNet
import random
import cupy as cp
import numpy as np2


fpath = "./idol/idol_result/idol_train_weight_2021-04-20 054113_8381.npz"
output_path = "./idol/idol_result/idol_train_weight_2021-04-20 054113_8381_np.npz"

load_data = dict(np2.load(fpath, allow_pickle=True))

print(type(load_data["Params"]))

print(load_data["Params"].item()["b18"])

for k, v in load_data.items():
    if k == "OtherParams" or k == "Params":
        for param_name in load_data.get(k).item():
            load_data[k].item()[param_name] = cp.asnumpy(load_data[k].item()[param_name])

np.savez_compressed(output_path, **load_data)

# print(load_data)