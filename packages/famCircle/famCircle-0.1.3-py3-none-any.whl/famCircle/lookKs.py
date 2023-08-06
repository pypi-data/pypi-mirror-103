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
from matplotlib.pyplot import MultipleLocator
from famCircle.bez import *
matplotlib.rcParams['font.sans-serif'] = ['KaiTi']

class lookKs():
    def __init__(self, options):
    ##### circle parameters
        # self.y1 = []
        # self.y2 = []
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readksfike(self):
        if self.model == 'YN00':
            upper = 99
            index_0 = 5
        elif self.model == 'NG86':
            upper = '-1'
            index_0 = 3
        else :
            print('model not found')
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
                    if float(row[index_0]) >= 0:
                        if float(row[index_0]) == upper: 
                            continue
                        ksl.append(float(row[index_0]))
                    else:
                        print(float(row[index_0]))
        return ksl

    def tj(self,min_ks,max_ks,step_number,step_size,kslist):
        li = []
        fenduan = {}
        for i in range(step_number):
            a = round((min_ks + i * step_size),5)
            li.append(a)
            name1 = round((a + a + step_size)/2,5)
            fenduan[name1] = 0
        # print(str(fenduan),li)
        for i in kslist:
            if i < min_ks or i >= max_ks:
                continue
            elif(i >= 0):
                for j in li:
                    if i >= j and i < j + step_size:
                        min1 = j
                        max1 = j + step_size
                        # print(min1,max1)
                        name = round((min1 + max1)/2,5)
                        # print(name)
                        fenduan[name] = fenduan[name] + 1
                    else:
                        continue
            else:
                continue
        return fenduan

    def run(self):
        kslist = self.readksfike()
        # print(kslist)
        step_size = float(self.step_size)
        if self.ks_concern == 'min,max':
            min_ks = min(kslist)
            max_ks = max(kslist)
        else:
            print(self.ks_concern)
            min_ks = float(self.ks_concern.split(',')[0])
            max_ks = float(self.ks_concern.split(',')[1])
        print(min_ks,max_ks)
        if ((max_ks - min_ks)/step_size) > int((max_ks - min_ks)/step_size):
            step_number = int((max_ks - min_ks)/step_size) + 1
            # min_ks = min_ks - ((max_ks - min_ks)/step_size - int((max_ks - min_ks)/step_size))/2
            # max_ks = max_ks - ((max_ks - min_ks)/step_size - int((max_ks - min_ks)/step_size))/2
            print(max_ks)
            max_ks = max_ks + ((max_ks - min_ks) - (int((max_ks - min_ks)/step_size)*step_size))
        else:
            step_number = int((max_ks - min_ks)/step_size)
        print(min_ks,max_ks)
        ksfd = self.tj(min_ks,max_ks,step_number,step_size,kslist)
        # print(ksfd)
        x1 = ksfd.keys()
        y = list(ksfd.values())
        # print(y)
        x = []

        for i in x1:
            x.append(i)
        # plt.tick_params(axis='both',which='major',labelsize=14)
        plt.xlabel('Ks')
        plt.ylabel('Richness')
        plt.plot(x,y,color='r', marker='.', linestyle='-', linewidth=0.5, markersize=0.5)
        c = round((max_ks-min_ks)/10,2)
        d = c/5
        x_major_locator=MultipleLocator(c)
        ax=plt.gca()
        #ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        #把x轴的主刻度设置为1的倍数
        # ax.yaxis.set_major_locator(y_major_locator)
        #把y轴的主刻度设置为10的倍数
        plt.xlim(min_ks - d, max_ks + d)
        #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
        # plt.ylim(-5,110)
        plt.savefig(self.savefile, dpi=300)

        sys.exit(0)
