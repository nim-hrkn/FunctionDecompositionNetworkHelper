#!/usr/bin/env python
# coding: utf-8

# 
#
#  (C) 2020 Hiori Kino
# 
# This software includes the work that is distributed in the Apache License 2.0
#
#

import pandas as pd
from graphviz import Digraph
import copy



class DecompositionTree:

    def __init__(self,basename = "caus"):
        if basename is None:
            basename = "caus"
        self.basename = basename
        
        self.method_prefix = "method_"
        
        self.edgelist = []
        self.invisedgelist = []
        self.boxnodelist = []
        self.sameranklist = []
        
    def next_itime(self,df,itime,imethod):
        for itime2 in range(itime+1,df.shape[1]):
            output2 = df.iloc[imethod,itime2]
            if output2==output2: # not isnan
                return itime2
        return None

    def prev_itime(self,df,itime,imethod):
        for itime2 in range(itime-1,-1,-1):
            output2 = df.iloc[imethod,itime2]
            if output2==output2: # not isnan
                return itime2
        return None
    
    def get_func_method_1(self,cell1,func_prefix="get_",method_prefix=None):
        cell1 = str(cell1)
        if cell1.find(":")<0:
            output1 = cell1
            way1 = cell1
        else:
            way1,output1 = cell1.split(":")
            if way1 is None:
                way1 = output1
        if method_prefix is None:
            method_prefix = self.method_prefix
                    
        if len(way1)>0:
            method1 = method_prefix+way1
        else:
            method1 = None
        if len(output1)>0:
            func1 = func_prefix+output1
        else:
            func1 = None
        return func1,method1

    def get_func_method_2(self,cell1,cell2):
        cell1 = str(cell1)
        cell2 = str(cell2)
        if cell2.find(":")<0:
            wayp = cell2
            output2 = cell2
        else:
            wayp,output2 = cell2.split(":")
            if output2 is None:
                output2 = wayp
                
        _,output1 = cell1.split(":")
        if len(output2)>0:
            funcp = "get_"+output2
        else:
            funcp = None
        if len(wayp)>0:
            methodp = self.method_prefix+wayp
        else:
            methodp = None
        if len(output1)>0:
            func1 = "get_"+output1
        else:
            func1 = None
        if len(wayp)>0:
            func2 = "apply_"+wayp    
        else:
            func2 = None
        return func1,func2,funcp,methodp

    def get_func_method_3(self,cell0,cell1,cell2):
        cell0 = str(cell0)
        cell1 = str(cell1)
        cell2 = str(cell2)
        if cell2.find(":")<0:
            wayp = cell2
            output2 = cell2
        else:
            wayp,output2 = cell2.split(":")
            if output2 is None:
                output2 = wayp
                
        _,output1 = cell1.split(":")
        _,output0 = cell0.split(":")
        
        if len(output2)>0:
            funcp = "get_"+output2
        else:
            funcp = None
        if len(wayp)>0:
            methodp = self.method_prefix+wayp
        else:
            methodp = NOne
        if len(output0)>0:
            func0 = "get_"+output0
        else:
            func0 = None
        if len(output1)>0:
            func1 = "get_"+output1
        else:
            func1 = None
        if len(wayp)>0:
            func2 = "apply_"+wayp    
        else:
            func2 = None
        return func0,func1,func2,funcp,methodp    
    
    def drop_dup(self,del_dup):
        if del_dup:
            self.edgelist = list(set(self.edgelist))
            self.invisedgelist = list(set(self.invisedgelist))
            self.boxnodelist = list(set(self.boxnodelist))
            self.sameranklist = list(set(self.sameranklist))

    def gen_tree(self,dot):
        edgelist = self.edgelist
        invisedgelist = self.invisedgelist
        boxnodelist = self.boxnodelist
        sameranklist = self.sameranklist
        
        for edge in edgelist:
            s = edge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dot.edge(x0,x1)
        for invisedge in invisedgelist:
            s = invisedge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dot.edge(x0,x1,style="invis")
                #dot.edge(x0,x1,style="dotted")
        for boxnode in boxnodelist:
            dot.node(boxnode,shape="box")
        for samerank in sameranklist:
            s = samerank.split(",")
            with dot.subgraph() as sub:
                sub.attr(rank="same")
                for x in s:
                    sub.node(x)
        return dot
    
    def causfirst_sparse2(self,df,dot=None):
        self.df = df

        edgelist = []
        invisedgelist = []
        boxnodelist = []
        sameranklist = []

        for imethod in range(df.shape[0]):
            itime = df.shape[1]
            while itime>0:
                itime = itime-1
                
                cell2 = df.iloc[imethod,itime]
                if cell2!=cell2 or cell2 is  None: #  isnan
                    continue
                if cell2.startswith("2)"):
                    #cell2 = cell2[2:] # delete 2), but leave it for debug now!
                    # search output1
                    itime1 = self.prev_itime(df,itime,imethod)
                    if itime1 is None:
                        continue
                    cell1 = df.iloc[imethod,itime1]
                    # serach output0
                    itime0 = self.prev_itime(df,itime1,imethod)
                    if itime0 is None:
                        continue
                    cell0 = df.iloc[imethod,itime0]
                    
                    func0,func1,func2,funcp,methodp = self.get_func_method_3(cell0,cell1,cell2)
                    print("3term",func0,func1,func2)
                    if funcp is not None and methodp is not None:
                        edgelist.append("{},{}".format(funcp,methodp))
                    if methodp is not None:
                        boxnodelist.append(methodp)
                    if methodp is not None and func0 is not None:
                        edgelist.append("{},{}".format(methodp,func0))                    
                    if methodp is not None and func1 is not None:
                        edgelist.append("{},{}".format(methodp,func1))
                    if methodp is not None and func2 is not None:
                        edgelist.append("{},{}".format(methodp,func2))
                    invisedgelist.append(",".join([func0,func1,func2]))
                    sameranklist.append(",".join([func0,func1,func2]))     
                    itime = itime-1
                    
                else:
                    # search output1
                    itime1 = self.prev_itime(df,itime,imethod)
                    if itime1 is None:
                        continue
                    cell1 = df.iloc[imethod,itime1]

                    func1,func2,funcp,methodp = self.get_func_method_2(cell1,cell2)
                    print("1({})({})({})({})".format(func1,func2,funcp,methodp))
                    if funcp is not None and methodp is not None:
                        edgelist.append("{},{}".format(funcp,methodp))
                    if methodp is not None:
                        boxnodelist.append(methodp)
                    if methodp is not None and func1 is not None:
                        edgelist.append("{},{}".format(methodp,func1))
                    if methodp is not None and func2 is not None:
                        edgelist.append("{},{}".format(methodp,func2))
                    if func1 is not None and func2 is not None:
                        invisedgelist.append(",".join([func1,func2]))
                        sameranklist.append(",".join([func1,func2]))

            for itime in range(df.shape[1]):
                cell1 = df.iloc[imethod,itime]
                if cell1==cell1 and cell1 is not None: # not isnan
                    cell1 = str(cell1)
                    func1,method1 = self.get_func_method_1(cell1)
                    print("1)({})({})".format(func1,method1))
                    if func1 is not None and method1 is not None:
                        edgelist.append("{},{}".format(func1,method1))
                        boxnodelist.append(method1)
        
        self.edgelist.extend(edgelist)
        self.invisedgelist.extend(invisedgelist)
        self.boxnodelist.extend(boxnodelist)
        self.sameranklist.extend(sameranklist)

    def create_tree(self,del_dup=True,dot=None):
    
        self.drop_dup(del_dup)
        
        if dot is None:
            dot = Digraph(self.basename)
        dot = self.gen_tree(dot)
        
        return dot


# In[10]:


import pandas as pd

def read_wffile(filename ):
    with open(filename) as f:
        lines = f.read()

    lines = lines.split("\n")

    # convert format 
    vlist = []
    for x in lines:
        if len(x)==0:
            continue
        x01 = x.split(":")
        x0 = x01[0]; x1=x01[1]
        s = x1.replace("]",":").replace("[",",")
        y = x0+s
        v = y.split(",")
        print(v)
        vlist.append(v)

    # make dataframe
    df = pd.DataFrame(vlist)

    # to change df.column
    col = []
    for i in range(df.shape[1]):
        if i==0:
            s = "method"
        else:
            s = "step{}".format(i)
        col.append(s)
        
    df.columns = col
    df.set_index("method",drop=True,inplace=True)
    return df



if __name__ == "__main__":
    import sys 
    import os

    basenamelist = sys.argv[1:]
    
    #basenamelist = ["Importance_GenerateGroup.wf",        "Importance_VisualizeRelevanceImportance.wf", "Importance_ExhaustiveSearchDOS.wf",      "Importance_MakeScores.wf", "Importance_ExhaustiveSearchDiagram.wf",  "Importance_RelevanceImportance.wf"]

                    
    print (basenamelist)

    if len(basenamelist)==0:
        sys.exit(1)

    if False:
        if len(basenamelist)>1:
            for name in basenamelist:
                fdt = DecompositionTree(name)
                base = os.path.split(name)[0]
                #df0 = pd.read_csv(name,index_col=[0])
                df0 = read_wffile(name)
                fdt.causfirst_sparse2(df0,"causSparse_"+base)
                dot = fdt.create_dot(del_dup=True)
                dot.format="png"
                dot.render(view=True)


    fdt = DecompositionTree("caus")
    for name in basenamelist:
        df0 = read_wffile(name)
        #df0 = pd.read_csv(name,index_col=[0])
        fdt.causfirst_sparse2(df0)
    dot = fdt.create_tree()
    dot.format="png"
    dot.render(view=True)

    print("done")






