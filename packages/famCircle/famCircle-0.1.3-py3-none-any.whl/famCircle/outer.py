### draw chromosome homology famCircle for eudicots with VV as reference, if VV is provided. If no vv chro is involved, it draws famCircle for other species
# -*- coding: UTF-8 -*-
import re
import os
import sys
import gc
from math import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse
from pylab import *
from famCircle.bez import *


class outer():
    def __init__(self, options):
    ##### circle parameters
        self.GAP_RATIO = 4 #gaps between chromosome circle, chr:gap = 4: 1
        self.radius = 0.33
        self.blocklength = 0.01 # radian 0.01
        self.block= 0.005 #block scize
        self.blockthick = 0.003 #0.006
        self.shiftratio = -2.1 # define the distance between overlapping glocks
        self.specieslist = []
        self.iscompletegenome = {}
        self.gene2pos={}# 基因起始位置
        self.chro2len = {}
        self.otherchrolist = []
        self.labels = []
        self.genes = []
        self.genepair2Ks = {}
        self.genepair2Ka = {}
        self.genepair0 = []
        self.peripheral = 'False'
        self.clusters = None
        self.start_list = []
        self.color = ['red', 'orangered', 'chocolate', 'orange', 'gold', 'yellow', 'yellowgreen', 'palegreen', 'limegreen', 'lime', 'aquamarine', 'teal', 'cyan', 'dodgerblue', 'royalblue', 'blueviolet', 'violet', 'fuchsia']
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def gene_length(self):
        # 读取基因长度，得到平均长度和最小最大长度
        f = open(self.gff,'r', encoding='utf-8')
        genelength = {}
        for row in f:
            if row[0] != '\n' and row[0] != '#':
                row = row.strip('\n').split('\t')
                # print(row)
                if str(row[1]) in genelength.keys():
                    continue
                if 'chr' == str(row[1])[3:6]:
                    continue
                length = abs(int(row[3]) - int(row[2]))
                genelength[str(row[1])] = length
        f.close()
        lt = []
        for i in genelength.values():
            lt.append(i)
        pj = sum(lt)/len(lt)
        return pj

    def readname(self, name):
        if ('^' in name):
            return name
        elif ('g' in name):
            name = name.replace('g', '^')
            return name

    def ksrun(self):
        # figurefile = "_".join(sys.argv[1:len(sys.argv)])+".genefam"
        fpchrolen = open(self.lens,'r', encoding='utf-8')
        fpgff = open(self.gff,'r', encoding='utf-8')
        fpgenefamilyinf = open(self.ks, 'r', encoding='utf-8')
        alphagenepairs = open(self.genepairs, 'r', encoding='utf-8')
        #### gene block parameters
        figure(1, (8, 8))  ### define the a square, or other rectangle of the figure, if to produce an oval here
        root =axes([0, 0, 1, 1])
        # chrolist = self.chrolist.split(',')
        chrolist = []
        for row in fpchrolen:
            chro = row.split('\t')[0]
            # print(chro)
            chrolist.append(chro)
        fpchrolen.close()
        for i in range(len(chrolist)):
            string = chrolist[i]
        #   print string[0:2]
            isnew = 1
            for sp in self.specieslist:
                if sp == string[0:2]:
                    isnew = 0
                    break
            if isnew==1:
                self.specieslist.append(string[0:2])
                if string == string[0:2]:
                    self.iscompletegenome[string[0:2]] = 1
                else:
                    self.iscompletegenome[string[0:2]] = 0

        ### input chromosome length
        # print(self.iscompletegenome.keys())
        fpchrolen = open(self.lens,'r', encoding='utf-8')
        for row in fpchrolen:
            chro,length = row.split('\t')[0],row.split('\t')[1]# 选择order或者end
            # sp = chro[:2].upper()
            sp = chro[:2]
            if self.iscompletegenome[sp] == 1 :
                self.chro2len[chro] = int(length)
                self.otherchrolist.append(chro)
            else:
                if chro in chrolist :
                    self.chro2len[chro] = int(length)
                    self.otherchrolist.append(chro)
        fpchrolen.close()
        ### full chro list
        for i in self.otherchrolist:
            self.labels.append(i)

        ## input gff
        # self.gene2pos={}
        # self.gene2chain = {}

        for row in fpgff:
            ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
            gene = self.readname(gene)
            if gene.split('^')[0] not in self.labels:
                continue
            start = int(start)
            end = int(end)
            self.gene2pos[gene] = int(start)
            # print(start)
            # self.gene2chain[gene] = int((end-start)/abs(end -start))# ？
            # print(int((end-start)/abs(end -start)))
        #    print gene, int(start), self.gene2chain
        fpgff.close()
        ### input gene family gene1 gene2 Ka Ks
        for row in fpgenefamilyinf:
            if (row.split()[0] == 'id1' or len(row.split()) < 4):
                continue
            gene1, gene2, Ka, Ks = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
            # print(gene1,'********************************')
            # print('1')
            gene1 = self.readname(gene1)
            gene2 = self.readname(gene2)
            if gene1.split('^')[0] not in self.labels or gene2.split('^')[0] not in self.labels:
                continue
            if (gene1 not in self.gene2pos.keys() or gene2 not in self.gene2pos.keys()):
                continue
            genepair = ""
            if gene1 < gene2:
               genepair = gene1 + " " + gene2
            else:
               genepair = gene2 + " " + gene1
            if len(gene1.split("^")[0]) < 10  and len(gene2.split("^")[0]) < 10 :
               self.genepair2Ka[genepair] = float(Ka)
               self.genepair2Ks[genepair] = float(Ks)
            if gene1 not in self.genes:
                self.genes.append(gene1)
            if gene2 not in self.genes :
                self.genes.append(gene2)
        fpgenefamilyinf.close()
        # print("genes ", self.genes, "genes")
        return root

    def rad_to_coord(self, angle, radius):
        return radius*cos(angle), radius*sin(angle)

    def to_deg(self, bp, total):
        # from basepair return as degree
        return bp*360./total

    def to_radian(self, bp, total):
        # from basepair return as radian
        # print ("to_radian", bp, total)
        return radians(bp*360./total)

    def plot_arc(self, start, stop, radius):
        # start, stop measured in radian 染色体
        #print start, stop
        t = arange(start, stop, pi/720.)
        x, y = radius*cos(t), radius*sin(t)
        plot(x, y, "k-",alpha=.5)

    def plot_cap(self, angle, clockwise):
        radius=self.sm_radius
        # angle measured in radian, clockwise is boolean 鸭舌
        if clockwise: 
            t = arange(angle, angle+pi, pi/30.)
        else: 
            t = arange(angle, angle-pi, -pi/30.)
        x, y = radius*cos(t), radius*sin(t)
        middle_r = (self.radius_a+self.radius_b)/2
        x, y = x + middle_r*cos(angle), y + middle_r*sin(angle)
        plot(x, y, "k-", alpha=.5)

    def plot_arc_block(self, start, radius):# block
        t = arange(start, start+self.block, pi/720.)
        x,y = radius * cos(t), radius*sin(t)
        x1, y1 = (radius-self.blockthick) * cos(t), (radius-self.blockthick) * sin(t)
        plot(x, y, "b-", alpha=0.5)
    #    plot(x1, y1, "g-", alpha=0.5)

        x0, y0 = radius*cos(start), radius*sin(start)
        x1,y1  = (radius-self.blockthick)*cos(start), (radius-self.blockthick)*sin(start)
    #    plot([x0, y0], [x1, y1], "g-", lw=0.2)

        x0, y0 = radius*cos(start+self.block), radius*sin(start+self.block)
        x1,y1  = (radius-self.blockthick)*cos(start+self.block), (radius-self.block)*sin(start+self.block)
    #    plot([x0, y0], [x1, y1], "g-", lw=0.2)

    def zj(self):
        fullchrolen = int(pd.DataFrame(self.chro2len.values()).sum())
        chr_number = len(self.labels) # total number of chromosomes
        GAP = fullchrolen/self.GAP_RATIO/chr_number # gap size in base pair
        total_size = fullchrolen + chr_number * GAP # base pairs 
        # print(total_size)
        for i in range(chr_number):
            self.start_list.append(0)
        for i in range(1, chr_number):
            self.start_list[i] = self.start_list[i-1] + self.chro2len[self.labels[i-1]] + GAP
        stop_list = [(self.start_list[i] + self.chro2len[self.labels[i]]) for i in range(chr_number)]
        # print(self.start_list)
        return stop_list, total_size, chr_number


    def transform_deg(self, ch, pos):
        return self.to_deg(pos + self.start_list[ch], total_size)

    def transform_pt(self, ch, pos, r, total_size):
        # convert chromosome position to axis coords
    #    print "transform", ch, pos, r
    #    print "startlist", self.start_list[ch]
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad)
    def transform_pt2(self, rad, r):
        return r*cos(rad), r*sin(rad)

    def plot_bez_inner(self, p1, p2, cl, total_size):
    #    print "inner"
        a, b, c = p1
        ex1x, ex1y = self.transform_pt(a, b, c, total_size)
        a, b, c = p2
        ex2x, ex2y = self.transform_pt(a, b, c, total_size)
        # Bezier ratio, controls curve, lower ratio => closer to center
        ratio = .5
        x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
        y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = Bezier(x, t)# 贝塞尔曲线
        yt = Bezier(y, t)
        plot(xt, yt, '-', color=cl, lw=.3, alpha=0.3)#alpha 透明度

    def plot_bez_outer(self, p1, p2, cl):
    #    print "outer"
        a, b, c = p1
        ex1x, ex1y = self.transform_pt(a, b, c, total_size)
        a, b, c = p2
        ex2x, ex2y = self.transform_pt(a, b, c, total_size)
        # Bezier ratio, controls curve, lower ratio => closer to center
        ratio = 1.1
        x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
        y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = Bezier(x, t)
        yt = Bezier(y, t)
        plot(xt, yt, '-', color=cl , lw=.1)

    def plot_bez_Ks(self, rad1, r1, rad2, r2, col):
    #    print "bez Ks 1"
        ex1x, ex1y = self.transform_pt2(rad1, r1)
        ex2x, ex2y = self.transform_pt2(rad2, r2)
        ratio = 0.5#0.5
        x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
        y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = Bezier(x, t)
        yt = Bezier(y, t)
        plot(xt, yt, '-', color=col, lw=.1)

    def plot_bez_Ks2(self, rad1, r1, rad2, r2, col, ratio):
    #    print "bez Ks 2"
        # print('rad1, r1',rad1, r1)
        ex1x, ex1y = self.transform_pt2(rad1, r1)
        ex2x, ex2y = self.transform_pt2(rad2, r2)
        # ratio = -0.7#0.5
        sita = pi / 2
        if ex1x != ex2x:
            sita = atan((ex2y-ex1y)/(ex2x-ex1x))
        d = sqrt((ex2x-ex1x)**2+(ex2y-ex1y)**2)
        L = d * ratio
        P1x = ex1x + L*sin(sita)
        P1y = ex1y - L*cos(sita)
        P2x = ex2x + L*sin(sita)
        P2y = ex2y - L*cos(sita)
        step = .01
        t = arange(0, 1+step, step)

        x=[ex1x, P1x, P2x, ex2x]
        y=[ex1y, P1y, P2y, ex2y]
        # print('x,y,t',x,y,t)
        xt = Bezier(x,t)
        yt = Bezier(y,t)
        plot(xt, yt, '-', color = col, lw = 0.3)#0.1

    def plot_sector(self, s, root):
        # self.zj()
        # block_id, chr_id, start_bp, stop_bp
        block_id, chr_id, start_bp, stop_bp = s
        theta0, theta1 = self.transform_deg(chr_id, start_bp), self.transform_deg(chr_id, stop_bp)
        dtheta = .1
        p1 = Wedge((0, 0), self.radius_a, theta0, theta1, dtheta=dtheta, fc="w", ec="w")
        p2 = Wedge((0, 0), self.radius_b, theta0, theta1, dtheta=dtheta, fc=colors[block_id], ec="w")
        root.add_patch(p2)
        root.add_patch(p1)

    def classify(self, Ks, start1, start2, grade):
        colorlist = ['red', 'lime', 'orange', 'chocolate', 'yellow', 'palegreen', 'teal', 'dodgerblue', 'blueviolet', 'fuchsia']
        lt = self.ks_concern.strip('\n').split(',')
        length = len(lt)
        if (Ks > eval(lt[-1]) or Ks < eval(lt[0])):
            color = 'gray'
            class1 = grade
            if (eval(self.peripheral) == 'True'):
                if (abs(start1 - start2) < eval(self.bridge)):
                    return color, class1
                else:
                    return None,None
            else:
                return None,None
        else:
            for i in range(length - 1):
                max = eval(lt[i + 1])
                if (Ks <= max):
                    if grade >= 9:
                        color = colorlist[9]
                    else:
                        color = colorlist[grade]
                    class1 = grade
                    if (abs(start1 - start2) < eval(self.bridge)):
                        return color, class1
                    else:
                        return None,None
                else:
                    continue

    def run(self):
        self.radius_a =  float(self.radius)
        self.radius_b = self.radius_a + 0.005#.33, .335   # 半径控制参数 
        self.sm_radius=(self.radius_b-self.radius_a)/2 #telomere capping
        if (os.path.exists(self.savecsv)):
            os.remove(self.savecsv)
        lt = ['gene1', 'gene2', 'start1', 'shift1', 'start2', 'shift2', 'class1', 'class2']
        with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file ,delimiter=',')
            writer.writerow(lt)
        root = self.ksrun()
        stop_list, total_size, chr_number = self.zj()
        alphagenepairs = open(self.genepairs, 'r', encoding='utf-8')
        ## sort gene according to lacation on circle
        genessorted = []
        geneno = 0
        for i in range(len(self.genes)):
            if geneno == 0:
                # print(self.genes[0])
                genessorted.append(self.genes[0])
                geneno = geneno + 1
            else:
                firstgene = genessorted[0]
                lastgene = genessorted[-1]
                chf = firstgene.split("^")[0]# 第一个基因的染色体
                chl = lastgene.split("^")[0]# 最后一个基因的染色体
                #print firstgene, lastgene, chf, chl, self.gene2pos[firstgene]
                posf = self.gene2pos[firstgene] + self.start_list[self.labels.index(chf)]
                posl = self.gene2pos[lastgene] + self.start_list[self.labels.index(chl)]
                chi = self.genes[i].split("^")[0]
                # print(chi)
                if (chi not in self.labels):
                    continue
                posi = self.gene2pos[self.genes[i]] + self.start_list[self.labels.index(chi)]
        #        print posf, posl, posi
                if posi <= posf:
                    genessorted[0:0] = [self.genes[i]]
                elif posi >= posl:
                    # print(self.genes[i])
                    genessorted.append(self.genes[i])
                else:
                    for j in range(len(genessorted)-1):
                        chj = genessorted[j].split("^")[0]
                        posj = self.gene2pos[genessorted[j]] + self.start_list[self.labels.index(chj)]
                        chj1 = genessorted[j+1].split("^")[0]
                        posj1 = self.gene2pos[genessorted[j+1]]+self.start_list[self.labels.index(chj1)]
                        #print posj, posj1, posi
                        if posi > posj and posi < posj1:
                            genessorted[j+1:j+1] = [self.genes[i]]
        #    print "genesort ", genessorted
        ##input genepairs inter sircle
        ###########
        ###########alpha genepairs
        ###########
        row = alphagenepairs.readline()#
        rowno = 0
        istoread = 0
        # print(self.labels)
        for row in alphagenepairs:

            id1, id2 = row.split()[0],row.split()[1]
            id1 = self.readname(id1)
            id2 = self.readname(id2)
            if id1.split('^')[0] not in self.labels or id2.split('^')[0] not in self.labels:
                continue
            self.genepair0.append(id1)
            self.genepair0.append(id2)
            pos1 = self.gene2pos[id1]
            pos2 = self.gene2pos[id2]
            chro1 = id1.split("^")[0]
            chro2 = id2.split("^")[0]
            # print(chro1,chro2)
            if(chro1 not in self.labels or chro2 not in self.labels):
                continue
            order1 = self.labels.index(chro1)
            order2 = self.labels.index(chro2)
            # print(order1, pos1, self.radius_a,order2, pos2, self.radius_a, "green", total_size)
            self.plot_bez_inner((order1, pos1, self.radius_a), (order2, pos2, self.radius_a), "green", total_size)
            rowno = rowno + 1
        alphagenepairs.close()

        # the chromosome layout
        j = 0
        for start, stop in zip(self.start_list, stop_list):
            start, stop = self.to_radian(start, total_size), self.to_radian(stop, total_size)
            # shaft
            self.plot_arc(start, stop, self.radius_a)
            self.plot_arc(start, stop, self.radius_b)

            # telemere capping
            clockwise=False
            self.plot_cap(start, clockwise)
            clockwise=True
            # print(start)
            self.plot_cap(stop, clockwise)
            
            # chromosome self.labels
            label_x, label_y = self.rad_to_coord((start+stop)/2, self.radius_b*0.9)#1.2
            #print label_x, label_y
            text(label_x, label_y, self.labels[j], horizontalalignment="center", verticalalignment="center", fontsize = 7, color = 'black')
            j+=1
        ########
        ########
        ### define shift level and draw gene blocks
        shiftlevel = 0
        gene2shift = {}
        gene2location = {}
        cho = genessorted[0].split("^")[0]
        pos0 = self.gene2pos[genessorted[0]] + self.start_list[self.labels.index(cho)]
        start = self.to_radian(pos0, total_size)
        # print(start)
        # print('3')
        # self.plot_arc_block(start, self.radius_a - shiftlevel * self.shiftratio * self.blockthick)
        gene2location[genessorted[0]]= start
        gene2shift[genessorted[0]] = shiftlevel
        laststart = start
        # print(genessorted[0])
        # self.genepair0.append(genessorted[0])

        for i in range(len(genessorted)):
            if genessorted[i] not in self.genepair0:
                continue
            chi = genessorted[i].split("^")[0]
            posi = self.gene2pos[genessorted[i]] + self.start_list[self.labels.index(chi)]
            # chain = self.gene2chain[genessorted[i]]
            start = self.to_radian(posi, total_size)
            if(start-laststart < self.blocklength):
                shiftlevel = shiftlevel + 1
            else:
                shiftlevel=0
            gene2location[genessorted[i]] = start
            gene2shift[genessorted[i]] = shiftlevel
            laststart = start
        ### draw Ks lines between genes
        gene_average = self.gene_length()
        for genepair in self.genepair2Ks.keys():
            gene1, gene2 = genepair.split(' ')
            # print(gene1, gene2)
            Ks = self.genepair2Ks[genepair]
            if gene1 not in gene2location.keys() or gene2 not in gene2location:
                continue# 此处还要修改
            if gene1 not in self.genepair0 or gene2 not in self.genepair0:#  筛选
                continue
            start1 = gene2location[gene1]
            shift1 = gene2shift[gene1]
            start2 = gene2location[gene2]
            shift2 = gene2shift[gene2]
            a=self.gene2pos[gene1]
            b=self.gene2pos[gene2]
            # print('a,b:',a,b) #  a,b: 45618718 48586752 基因起始位置
            pitch = abs(b-a)
            grade = int(pitch / (eval(self.series) * gene_average))# 分级
            color, class1 = self.classify(Ks, start1, start2, grade)
            ratio = 0.5

            if (color != None):
                if (self.clusters == 'None'):
                    lt = [gene1, gene2, start1, shift1, start2, shift2, class1]
                    with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                        writer = csv.writer(file ,delimiter=',')
                        writer.writerow(lt)
                    self.plot_bez_Ks2(start1, self.radius_a - (shift1+1) * self.shiftratio * self.blockthick, start2, self.radius_a - (shift2+1) * self.shiftratio * self.blockthick, color, ratio)
                else:
                    # print(self.color[4])
                    class2 = self.clusters
                    self.plot_bez_Ks2(start1, self.radius_a - (shift1+1) * self.shiftratio * self.blockthick, start2, self.radius_a - (shift2+1) * self.shiftratio * self.blockthick, self.color[4], ratio)
                    lt = [gene1, gene2, start1, shift1, start2, shift2, class1, class2]
                    with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                        writer = csv.writer(file ,delimiter=',')
                        writer.writerow(lt)            
            else :
                # print('间距不达标')
                pass

        ### Again: define shift level and draw gene blocks
        shiftlevel = 0
        gene2shift = {}
        gene2location = {}
        cho = genessorted[0].split("^")[0]
        pos0 = self.gene2pos[genessorted[0]] + self.start_list[self.labels.index(cho)]
        start = self.to_radian(pos0, total_size)
        # print('4')
        # self.plot_arc_block(start, self.radius_a - shiftlevel * self.shiftratio * self.blockthick)
        #gene2location[genessorted[0]]= start
        #gene2shift[genessorted[0]] = shiftlevel
        laststart = start
        # self.genepair0.append(genessorted[0])# 
        # print('2')
        for i in range(len(genessorted)):## 单独循环
            chi = genessorted[i].split("^")[0]
            if genessorted[i] not in self.genepair0:#  筛选
                continue
            posi = self.gene2pos[genessorted[i]] + self.start_list[self.labels.index(chi)]
            # chain = self.gene2chain[genessorted[i]]
            start = self.to_radian(posi, total_size)
            # print('start',start)
            if(start-laststart<self.blocklength):
                # print('start-laststart<self.blocklength',start-laststart,self.blocklength)
                shiftlevel = shiftlevel + 1
            else:
                shiftlevel=0
            self.plot_arc_block(start, self.radius_a - (shiftlevel+1) * self.shiftratio * self.blockthick)# 主要的块儿来源
            laststart = start
        #### draw tick showing scale of chromosomes
        for i in range(chr_number):
            pos = 0
            while pos < self.chro2len[self.labels[i]]:

                xx1, yy1 = self.transform_pt(i, int(pos), self.radius_b, total_size)
                xx2, yy2 = self.transform_pt(i, int(pos), self.radius_b-0.003, total_size)
                plot([xx1, xx2], [yy1, yy2], "k-", lw = .2)
                pos = pos + 10000000
        # print('3')
        root.set_xlim(-.8, .8)#-.5, .5
        root.set_ylim(-.8, .8)
        root.set_axis_off()
        savefig(self.savefile, dpi=1000)
        sys.exit(0)
