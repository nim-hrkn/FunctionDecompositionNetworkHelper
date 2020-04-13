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

        
class DecompositionTree(object):

    def __init__(self,basename = "caus"):
        if basename is None:
            basename = "caus"
        self.basename = basename
        
        self.method_prefix = "method_"
        self.func_prefix = "get_"
        self.applymethod_prefix = "apply_"

        self.invisstyle = "invis"
        
        self.edgelist = []
        self.invisedgelist = []
        self.boxnodelist = []
        self.sameranklist = []
        
    def check_extension(self,name,ext=None):
        if ext is None:
            # check file extension
            basename,ext = os.path.splitext(name)
            ext = ext[1:] # delete the first dottree 
        return ext

    def drop_dup(self,del_dup):
        if del_dup:
            self.edgelist = list(set(self.edgelist))
            self.invisedgelist = list(set(self.invisedgelist))
            self.boxnodelist = list(set(self.boxnodelist))
            self.sameranklist = list(set(self.sameranklist))

    def gen_tree(self,dottree,del_dup=True):
        self.drop_dup(del_dup)
        edgelist = self.edgelist
        invisedgelist = self.invisedgelist
        boxnodelist = self.boxnodelist
        sameranklist = self.sameranklist
        

        for edge in edgelist:
            s = edge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dottree.edge(x0,x1)
        for invisedge in invisedgelist:
            s = invisedge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dottree.edge(x0,x1,style=self.invisstyle)
        for boxnode in boxnodelist:
            dottree.node(boxnode,shape="box")
        for samerank in sameranklist:
            s = samerank.split(",")
            with dottree.subgraph() as sub:
                sub.attr(rank="same")
                for x in s:
                    sub.node(x)
        return dottree

    def create_tree(self,dottree=None):
        if dottree is None:
            dottree = Digraph(self.basename)

        dottree = self.gen_tree(dottree)
        return dottree
 
class taxologyWay(DecompositionTree):
    def __init__(self,basename="taxo"):

        super().__init__(basename)

        self.den_edgelist = []

        self.excludenodelist = []
        self.data = None

    def load(self,filename):
        data = None
        with open(filename) as f:
            data = yaml.safe_load(f)
        self.data = data


    def create_dendrogram(self,dot=None):
        den_edgelist = self.den_edgelist 
        print(den_edgelist)
        if dot is None:
            dot = Digraph(self.basename)
            dot.graph_attr["rankdir"] = "TB"
        for den in den_edgelist:
            print(den)
            dot.edge(den[0],den[1])
            dot.node(den[0],shape="box")
            dot.node(den[1],shape="box")
        return dot

    def gen_connection_method_method(self,methodlist,pmethodname=None,pnodetype=None):
        if methodlist is None:
            return 

        if pmethodname is not None:
            pnodename = pmethodname
            for methodline in methodlist:
                name = methodline["name"]
                self.den_edgelist.append([pnodename,name])

        if pmethodname is None:
            for methodline in methodlist:
                print("methodline>",methodline)
                name = methodline["name"]
                if "method" in methodline.keys():
                    method = methodline["method"]
                else:
                    method = None
                if "nodetype" in methodline.keys():
                    nodetype = methodline["nodetype"]
                else:
                    nodetype = None
                self.gen_connection_method_method(method,name,nodetype)
        else:
            if pnodetype == "PartOf" or pnodetype is None:
                funcnamelist = []
                for methodline in methodlist:
                    name = methodline["name"]

                    #funcp->methodp edge
                    funcp = self.func_prefix + pmethodname
                    methodp = self.method_prefix + pmethodname 

                    if pmethodname not in self.excludenodelist:
                        self.edgelist.append(",".join([ funcp,methodp]) ) 
                    self.boxnodelist.append(methodp)

                    print(pnodetype,name,",".join([ funcp,methodp]) )

                    #methodp->func edge
                    func1 = self.func_prefix+ name
                    self.edgelist.append(",".join([methodp,func1]))

                    funcnamelist.append(func1)

                    if "nodetype" in methodline.keys():
                        nodetype = methodline["nodetype"]
                    else:
                        nodetype = None
                    if "method" in methodline.keys():
                        method = methodline["method"]
                    else:
                        method = None
                   
                    self.gen_connection_method_method(method,name,nodetype)

                applyp = self.applymethod_prefix + pmethodname
                self.edgelist.append(",".join([methodp,applyp]))
                funcnamelist.append(applyp)
                self.invisedgelist.append(",".join(funcnamelist))
                self.sameranklist.append(",".join(funcnamelist))

            elif pnodetype == "IsA":

                namelist = []
                for methodline in methodlist:
                    name = methodline["name"]
                    if "nodetype" in methodline.keys():
                        nodetype = methodline["nodetype"]
                    else:
                        nodetype = None
                    print(">>",pmethodname,pnodetype,name,nodetype)
                    #self.excludenodelist.append(name) 
                    namelist.append(name)

                    #funcp->methodp edge
                    funcp = self.func_prefix + pmethodname
                    methodp = self.method_prefix + pmethodname
                    func1 = self.func_prefix+ name
                    method1 = self.method_prefix+ name

                    if nodetype is None:
                        self.edgelist.append(",".join([funcp,method1]))
                        self.boxnodelist.append(method1)
                    else:
                        self.edgelist.append(",".join([funcp,methodp]))
                        self.edgelist.append(",".join([methodp,func1]))
                        self.boxnodelist.append(methodp)

                    if "method" in methodline.keys():
                        method = methodline["method"]
                    else:
                        method = None
                   
                    self.gen_connection_method_method(method,name,nodetype)
                    
    def methodtree(self):
        data = self.data
        self.gen_connection_method_method(data["method"])

        
class workFlowWay(DecompositionTree):

    def __init__(self,basename = "caus"):

        super().__init__(basename)

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
   

    def gen_workflow(self,dottree):
        print("gen_workflow")
        print(self.wf_edgelist)
        dottree.graph_attr["rankdir"] = "BT" #"LR"
        edgelist = self.wf_edgelist
        boxnodelist = self.wf_boxnodelist
        invisnodelist = self.wf_invisnodelist
        for edge in edgelist:
            s = edge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dottree.edge(x0,x1)
        for boxnode in boxnodelist:
            dottree.node(boxnode,shape="box")
        for invisnode in invisnodelist:
            dottree.node(invisnode,color="white")
        print(dottree)
        return dottree 
    
    def nodes2funcs(self,nodes):
        funcs = []
        for node in nodes:
            funcs.append(self.func_prefix+node)
        return funcs

    def causfirst_sparse2(self,dottree=None):
        df = self.df

        edgelist = []
        invisedgelist = []
        boxnodelist = []
        sameranklist = []

        wf_edgelist = []
        wf_boxnodelist = []
        wf_invisnodelist = []

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

    def drop_dup_wf(self,del_up):
        if del_up:
            self.wf_edgelist = list(set(self.wf_edgelist))
            self.wf_boxnodelist = list(set(self.wf_boxnodelist))
            self.wf_invisnodelist = list(set(self.wf_invisnodelist))

    def create_workflow(self,del_dup=True,dot=None):
    
        self.drop_dup_wf(del_dup)
        
        if dot is None:
            dot = Digraph(self.basename)
        dot = self.gen_workflow(dot)
        
        return dot


    def convert_wf_to_csv(self,lines):
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

    def read_wffile(self,filename ):
        with open(filename) as f:
            lines = f.read()

        lines = lines.split("\n")
        vlist = self.convert_wf_to_csv(lines)

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

    def load(self,name,ext=None):
        if ext is None:
            ext = self.check_extension(name)

        df0 = None
        if ext == "csv":
            df0 = pd.read_csv(name,index_col=[0])
        elif ext == "wf":
            df0 = self.read_wffile(name)
        else:
            print("extension",ext,"not supported.")
        self.df = df0 

if __name__ == "__main__":
    import sys 
    import os

    namelist = sys.argv[1:]
                    
    print (namelist)

    if len(namelist)==0:
        sys.exit(1)

    dottree = Digraph("caus")

    for filename in namelist:

        basename,ext = os.path.splitext(filename)
        ext = ext[1:]

        if ext in ["yml"]:
            taxo = taxologyWay()
            taxo.load(filename)
            taxo.methodtree()
            dottree = taxo.create_tree(dottree)

            if True:
                dotwf = Digraph("den_"+basename)
                dotwf = taxo.create_dendrogram(dot=dotwf)
                dotwf.format = "png"
                dotwf.render(view=True)
    
        if ext in ["wf", "csv"]:
            wf = workFlowWay()
            wf.load(filename)
            wf.causfirst_sparse2()
            dottree = wf.create_tree(dottree)
            if True:
                dotwf = Digraph("wf_"+basename)
                dotwf = wf.create_workflow(dot=dotwf)
                dotwf.format = "png"
                dotwf.render(view=True)
 
    dottree.format = "png"
    dottree.render(view=True)
    


    print("done")


