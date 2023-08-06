### draw chromosome homology famCircle for eudicots with VV as reference, if VV is provided. If no vv chro is involved, it draws famCircle for other species
# -*- coding: UTF-8 -*-


import re
import sys
from math import *
from scipy import interpolate
import pylab as pl
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

class lookKs():
    def __init__(self, options):
    ##### circle parameters
        # self.y1 = []
        # self.y2 = []
        self.Ks_concern = 'min,max'
        self.step_size = 0.05
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readksfike(self):
        ksl = []
        f = open(self.ks, 'r', encoding='utf-8')
        for row in f:
            if (row == '\n' or row[0] == '#'):
                continue
            else:
                row = row.strip('\n').split('\t')
                if str(row[0]) == 'id1':
                    continue
                else:
                    ksl.append(float(row[3]))
        return ksl

    def tj(self,min_ks,max_ks,step_number,step_size,kslist):
        li = []
        fenduan = {}
        for i in range(step_number):
            a = round((min_ks + i * step_size),3)
            li.append(a)
            name1 = round((a + a + step_size)/2,3)
            fenduan[name1] = 0
        # print(str(fenduan),li)
        for i in kslist:
            if i < min_ks or i >= max_ks:
                continue
            else:
                for j in li:
                    if i >= j and i < j + step_size:
                        min1 = j - step_size
                        max1 = j
                        print(min1,max1)
                        name = round((min1 + max1)/2,3)
                        print(name)
                        fenduan[name] = fenduan[name] + 1
                    else:
                        continue
        return fenduan
    def gaussian(self,x,*param):
        return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+\
               param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))
         
    def run(self):
        kslist = self.readksfike()
        step_size = float(self.step_size)
        if self.Ks_concern == 'min,max':
            min_ks = min(kslist)
            max_ks = max(kslist)
        else:
            min_ks = float(self.Ks_concern.split(',')[0])
            max_ks = float(self.Ks_concern.split(',')[1])
        if ((max_ks - min_ks)/step_size) > int((max_ks - min_ks)/step_size):
            step_number = int((max_ks - min_ks)/step_size) + 1
            min_ks = min_ks - ((max_ks - min_ks)/step_size - int((max_ks - min_ks)/step_size))/2
            max_ks = max_ks - ((max_ks - min_ks)/step_size - int((max_ks - min_ks)/step_size))/2
        else:
            step_number = int((max_ks - min_ks)/step_size)
        ksfd = self.tj(min_ks,max_ks,step_number,step_size,kslist)
        print(ksfd)
        x = ksfd.keys()
        y = ksfd.values()

        plt.figure(figsize=(10, 6), dpi=300)
        plt.scatter(x, y, s=0.1, c='b', marker='.')
        savefig(self.savefile, dpi=500)


        # import numpy as np
        # import pylab as plt
        #import matplotlib.pyplot as plt
        from scipy.optimize import curve_fit
        from scipy import asarray as ar,exp
        x1 = []
        y1 = []
        for i in x:
        	x1.append(i)
        for i in y:
        	y1.append(i)
        x = ar(x1)
        y = ar(y1)
        
        popt,pcov = curve_fit(self.gaussian,x,y,p0=[3,4,3,6,1,1])
        print(popt)
        print(pcov)
         
        plt.plot(x,y,color='b', marker='.', linestyle='-.', linewidth=0.01, markersize=0.01,label='data')
        plt.plot(x,self.gaussian(x,*popt),color='r', marker='.', linestyle='-.', linewidth=0.1, markersize=0.1,label='fit')
        plt.legend()
        plt.savefig('xx.png', dpi=500)

        sys.exit(0)