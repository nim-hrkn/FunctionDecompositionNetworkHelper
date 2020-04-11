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

import sys
import yaml

class taxologyWay:
    def __init__(self,basename="base"):
        self.wflist = []
        self.nodeorderlist = []

    def load(self,filename):
        data = None
        with open(filename) as f:
            data = yaml.safe_load(f)
        print(data)
        return data

    def gen_connection_method_method(self,methodlist,pmethod=None):
        if methodlist is None:
            return None,None
        namelist = []
        for methodline in methodlist:
            name = methodline["name"]
            namelist.append(name)
            try:
                method = methodline["method"]
            except:
                method = None

            print("m>",pmethod,name)
            if pmethod is not None:
                self.wflist.append("dummy:[{0}]{0}[{1}]{1}".format(name,pmethod))
            
            mlistnew = self.gen_connection_method_method(method,name)
        self.nodeorderlist.append(",".join(namelist))

    def gen_wf(self,filename):
        data = self.load(filename)
        _ = self.gen_connection_method_method(data["method"])

        print(self.wflist)
        print(self.nodeorderlist)
        return self.wflist,self.nodeorderlist 




class DecompositionTree:

    def __init__(self,basename = "caus"):
        if basename is None:
            basename = "caus"
        self.basename = basename
        
        self.method_prefix = "method_"
        self.func_prefix = "get_"
        self.applymethod_prefix = "apply_"
        
        self.edgelist = []
        self.invisedgelist = []
        self.boxnodelist = []
        self.sameranklist = []

        self.wf_edgelist = []
        self.wf_boxnodelist = []
        self.wf_invisnodelist = []
        
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
    
    def get_func_method_1(self,cell1,func_prefix=None,method_prefix=None):
        if func_prefix is None:
            func_prefix = self.func_prefix 
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
            funcp = self.func_prefix+output2
        else:
            funcp = None
        if len(wayp)>0:
            methodp = self.method_prefix+wayp
        else:
            methodp = None
        if len(output1)>0:
            func1 = self.func_prefix+output1
        else:
            func1 = None
        if len(wayp)>0:
            func2 = self.applymethod_prefix+wayp    
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
            funcp = self.func_prefix+output2
        else:
            funcp = None
        if len(wayp)>0:
            methodp = self.method_prefix+wayp
        else:
            methodp = NOne
        if len(output0)>0:
            func0 = self.func_prefix+output0
        else:
            func0 = None
        if len(output1)>0:
            func1 = self.func_prefix+output1
        else:
            func1 = None
        if len(wayp)>0:
            func2 = self.applymethod_prefix+wayp    
        else:
            func2 = None
        return func0,func1,func2,funcp,methodp    
 
    def get_wf_method_1(self,cell0):
        cell0 = str(cell0)
        way0,output0 = cell0.split(":")
        if len(way0)==0:
            way0 = None
        if len(output0)==0:
            output0 = None
        return way0,output0

    def get_wf_method_2(self,cell0,cell1):
        cell0 = str(cell0)
        cell1 = str(cell1)
        way0,output0 = cell0.split(":")
        way1,output1 = cell1.split(":")
        if len(way0)==0:
            way0 = None
        if len(output0)==0:
            output0 = None
        if len(way1)==0:
            way1 = None
        if len(output1)==0:
            ouptut1 = None
        return way0,output0,way1,output1
 
    def get_wf_method_3(self,cell0,cell1,cell2):
        cell0 = str(cell0)
        cell1 = str(cell1)
        cell2 = str(cell2)
        way0,output0 = cell0.split(":")
        way1,output1 = cell1.split(":")
        way2,output2 = cell2.split(":")
        if len(way0)==0:
            way0 = None
        if len(output0)==0:
            output0 = None
        if len(way1)==0:
            way1 = None
        if len(output1)==0:
            ouptut1 = None
        if len(way2)==0:
            way2 = None
        if len(output2)==0:
            ouptut2 = None
        return way0,output0,way1,output1,way2,output2
   
    def drop_dup(self,del_dup):
        if del_dup:
            self.edgelist = list(set(self.edgelist))
            self.invisedgelist = list(set(self.invisedgelist))
            self.boxnodelist = list(set(self.boxnodelist))
            self.sameranklist = list(set(self.sameranklist))
            self.wf_edgelist = list(set(self.wf_edgelist))
            self.wf_boxnodelist = list(set(self.wf_boxnodelist))
            self.wf_invisnodelist = list(set(self.wf_invisnodelist))

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


    def gen_workflow(self,dot):
        dot.graph_attr["rankdir"] = "BT" #"LR"
        edgelist = self.wf_edgelist
        boxnodelist = self.wf_boxnodelist
        invisnodelist = self.wf_invisnodelist
        for edge in edgelist:
            s = edge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dot.edge(x0,x1)
        for boxnode in boxnodelist:
            dot.node(boxnode,shape="box")
        for invisnode in invisnodelist:
            dot.node(invisnode,color="white")

        return dot 
    
    def nodes2funcs(self,nodes):
        funcs = []
        for node in nodes:
            funcs.append(self.func_prefix+node)
        return funcs

    def causfirst_sparse2(self,df,node_orderlist=None,dot=None):
        self.df = df

        edgelist = []
        invisedgelist = []
        boxnodelist = []
        sameranklist = []

        wf_edgelist = []
        wf_boxnodelist = []
        wf_invisnodelist = []

        if True:
            if node_orderlist is not None:
                for nodes in node_orderlist:
                    nodes = nodes.split(",")
                    print("order",nodes)
                    funcs = self.nodes2funcs(nodes)     
                    invisedgelist.append(",".join(funcs))

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

                    # workflow edge
                    way0,output0,way1,output1,way2,output2 = self.get_wf_method_3(cell0,cell1,cell2)
                    if way0 is not None and output0 is not None:
                        wf_edgelist.append(",".join([way0,output0]))
                        wf_boxnodelist.append(way0)
                        wf_invisnodelist.append(output0)
                    if way1 is not None and output1 is not None:
                        wf_edgelist.append(",".join([way1,output1]))
                        wf_boxnodelist.append(way1)
                        wf_invisnodelist.append(output1)
                    if way2 is not None and output2 is not None:
                        wf_edgelist.append(",".join([way2,output2]))
                        wf_boxnodelist.append(way2)
                        wf_invisnodelist.append(output2)
                    if output0 is not None and output1 is not None and output2 is not None and way2 is not None:
                        wf_edgelist.append(",".join([output0,way2]))
                        wf_edgelist.append(",".join([output1,way2]))
                        wf_edgelist.append(",".join([way2,output2]))

                    itime = itime-1
                    
                else:
                    # search output1
                    itime1 = self.prev_itime(df,itime,imethod)
                    if itime1 is None:
                        continue
                    cell1 = df.iloc[imethod,itime1]

                    func1,func2,funcp,methodp = self.get_func_method_2(cell1,cell2)
                    #print("1({})({})({})({})".format(func1,func2,funcp,methodp))
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

                    # workflow edge
                    way0,output0,way1,output1 = self.get_wf_method_2(cell1,cell2)
                    if way0 is not None and output0 is not None:
                        wf_edgelist.append(",".join([way0,output0]))
                        wf_boxnodelist.append(way0)
                        wf_invisnodelist.append(output0)
                    if way1 is not None and output1 is not None:
                        wf_edgelist.append(",".join([way1,output1]))
                        wf_boxnodelist.append(way1)
                        wf_invisnodelist.append(output1)
                    if output0 is not None and output1 is not None and way1 is not None:
                        wf_edgelist.append(",".join([output0,way1]))
                        wf_edgelist.append(",".join([way1,output1]))


            for itime in range(df.shape[1]):
                cell1 = df.iloc[imethod,itime]
                if cell1==cell1 and cell1 is not None: # not isnan
                    cell1 = str(cell1)
                    func1,method1 = self.get_func_method_1(cell1)
                    print("1)({})({})".format(func1,method1))
                    if func1 is not None and method1 is not None:
                        edgelist.append("{},{}".format(func1,method1))
                        boxnodelist.append(method1)
                    way1,output1 = self.get_wf_method_1(cell1)
                    if output1 is not None:
                        wf_invisnodelist.append(output1)
                    if way1 is not None and output1 is not None:
                        wf_edgelist.append(",".join([way1,output1]))
                        wf_boxnodelist.append(way1)
                        
        
        self.edgelist.extend(edgelist)
        self.invisedgelist.extend(invisedgelist)
        self.boxnodelist.extend(boxnodelist)
        self.sameranklist.extend(sameranklist)

        self.wf_edgelist.extend(wf_edgelist)
        self.wf_boxnodelist.extend(wf_boxnodelist)
        self.wf_invisnodelist.extend(wf_invisnodelist)

    def create_tree(self,del_dup=True,dot=None):
    
        self.drop_dup(del_dup)
        
        if dot is None:
            dot = Digraph(self.basename)
        dot = self.gen_tree(dot)
        
        return dot

    def create_workflow(self,del_dup=True,dot=None):
    
        self.drop_dup(del_dup)
        
        if dot is None:
            dot = Digraph(self.basename)
        dot = self.gen_workflow(dot)
        
        return dot



# In[10]:


import pandas as pd

def convert_wf_to_csv(lines):
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
        vlist.append(v)
    print(lines)
    print(vlist)
    return vlist

def read_wffile(filename ):
    with open(filename) as f:
        lines = f.read()

    lines = lines.split("\n")
    vlist = convert_wf_to_csv(lines)

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

def read_ymlfile(filename):
    wf = taxologyWay() 
    wflist,nodeorderlist = wf.gen_wf(filename)

    vlist = convert_wf_to_csv(wflist)

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
    return df,nodeorderlist


def read_file(name,filetype=None):
    if filetype is None:
        # check file extension
        basename,ext = os.path.splitext(name)
        ext = ext[1:]
    print("ext({})".format(ext))
    node_orderlist = None
    if ext == "csv":
        df0 = pd.read_csv(name,index_col=[0])
    elif ext == "wf":
        df0 = read_wffile(name)
    elif ext == "yml" or ext == "yaml":
        df0,node_orderlist = read_ymlfile(name)
    return df0,node_orderlist

if __name__ == "__main__":
    import sys 
    import os

    basenamelist = sys.argv[1:]
                    
    print (basenamelist)

    if len(basenamelist)==0:
        sys.exit(1)

#    if False:
#        if len(basenamelist)>1:
#            for name in basenamelist:
#                fdt = DecompositionTree(name)
#                base = os.path.split(name)[0]
#                df0 = read_file(name)
#                fdt.causfirst_sparse2(df0,"causSparse_"+base)
#                dot = fdt.create_dot(del_dup=True)
#                dot.format="png"
#                dot.render(view=True)


    fdt = DecompositionTree("caus_wf")
    for name in basenamelist:
        df0,node_orderlist = read_file(name)
        fdt.causfirst_sparse2(df0)
    dot = fdt.create_workflow()
    dot.format="png"
    dot.render(view=True)

    fdt = DecompositionTree("caus_tree")
    for name in basenamelist:
        df0,node_orderlist = read_file(name)
        fdt.causfirst_sparse2(df0,node_orderlist)
    dot = fdt.create_tree()
    dot.format="png"
    dot.render(view=True)


    print("done")






