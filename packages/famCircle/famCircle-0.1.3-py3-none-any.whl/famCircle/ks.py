### draw chromosome homology famCircle for eudicots with VV as reference, if VV is provided. If no vv chro is involved, it draws famCircle for other species
# -*- coding: UTF-8 -*-


import re
import sys
from math import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse
from pylab import *
from scipy.optimize import curve_fit
import math
import matplotlib.mlab as mlab
from scipy.stats import norm

from famCircle.bez import *
matplotlib.rcParams['font.sans-serif'] = ['KaiTi']

class ks():
    def __init__(self, options):
    ##### circle parameters
        # self.y1 = []
        # self.y2 = []
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readksfike(self):
    	