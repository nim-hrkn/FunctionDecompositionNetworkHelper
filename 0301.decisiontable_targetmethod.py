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

    def __init__(self,df):
        self.df = df

        self.method_prefix = "method_"

    def next_itime(self,df,itime,imethod):
        for itime2 in range(itime+1,df.shape[1]):
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
            output1,way1 = cell1.split(":")
            if way1 is None:
                way1 = output1
        if method_prefix is None:
            method_prefix = self.method_prefix
        method1 = method_prefix+way1
        func1 = func_prefix+output1
        return func1,method1

    def get_func_method_2(self,cell1,cell2):
        cell1 = str(cell1)
        cell2 = str(cell2)
        if cell2.find(":")<0:
            wayp = cell2
            output2 = cell2
        else:
            output2,wayp = cell2.split(":")
            if wayp is None:
                wayp = output2
        output1,_ = cell1.split(":")
        funcp = "get_"+output2
        methodp = self.method_prefix+wayp
        func1 = "get_"+output1
        func2 = "apply_"+wayp    
        return func1,func2,funcp,methodp
    
    def drop_dup(self):
        if self.del_dup:
            self.edgelist = list(set(self.edgelist))
            self.invisedgelist = list(set(self.invisedgelist))
            self.boxnodelist = list(set(self.boxnodelist))
            self.sameranklist = list(set(self.sameranklist))

    def gen_dot(self,dot):
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
    
    
    def causfirst_sparse(self,basename,del_dup,dot=None):
        df = self.df
        self.del_dup = del_dup


        edgelist = []
        invisedgelist = []
        boxnodelist = []
        sameranklist = []

        for imethod in range(df.shape[0]):
            for itime in range(df.shape[1]):
                
                cell1 = df.iloc[imethod,itime]
                if cell1!=cell1: #  isnan
                    continue
                # search output2
                itime2 = self.next_itime(df,itime,imethod)
                if itime2 is None:
                    continue
                cell2 = df.iloc[imethod,itime2]

                func1,func2,funcp,methodp = self.get_func_method_2(cell1,cell2)

                edgelist.append("{},{}".format(funcp,methodp))
                boxnodelist.append(methodp)
                edgelist.append("{},{}".format(methodp,func1))
                edgelist.append("{},{}".format(methodp,func2))
                invisedgelist.append("{},{}".format(func1,func2))
                #if itime+1 ==itime2:
                if True:
                    sameranklist.append("{},{}".format(func1,func2))

        for imethod in range(df.shape[0]):
            for itime in range(df.shape[1]):
                cell1 = df.iloc[imethod,itime]
                if cell1==cell1: # not isnan
                    cell1 = str(cell1)

                    func1,method1 = self.get_func_method_1(cell1)

                    edgelist.append("{},{}".format(func1,method1))
                    boxnodelist.append(method1)
                    break

        
        self.edgelist = edgelist
        self.invisedgelist = invisedgelist
        self.boxnodelist = boxnodelist
        self.sameranklist = sameranklist
        
        self.drop_dup()
        
        if dot is None:
            dot = Digraph(basename,filename=basename)
        dot = self.gen_dot(dot)
        
        return dot

    
    
    def funcfirst(self,basename,del_dup=True,dot=None):
        df = self.df
        self.del_dup = del_dup

        edgelist = []
        boxnodelist = []
        invisedgelist = []
        sameranklist = []
 
        wayp = df.index.name
        cell1 = wayp
        funcp,methodp = self.get_func_method_1(cell1)
        methodlist = df.index.to_list()

        funclist = df.columns.to_list()
        
        edgelist.append(",".join([funcp,methodp]))
        boxnodelist.append(methodp)
        for f in funclist:
            edgelist.append(",".join([methodp,f]))        
        invisedgelist.append(",".join(funclist))
        sameranklist.append(",".join(funclist))
        
        for itime in range(df.shape[1]):
            methodlist = []
            applylist = []
            funcp = funclist[itime]
            for imethod in range(df.shape[0]):
                cell1 = df.iloc[imethod,itime]
                if cell1!=cell1: 
                    continue
                func1,meth1 = self.get_func_method_1(cell1,func_prefix="apply_")
                edgelist.append(",".join([funcp,meth1]))
                boxnodelist.append(meth1)

        self.edgelist = edgelist
        self.invisedgelist = invisedgelist
        self.boxnodelist = boxnodelist
        self.sameranklist = sameranklist
        
        
        self.drop_dup()
        
        if dot is  None:
            dot = Digraph(basename,filename=basename)        
        
        dot = self.gen_dot(dot)
        
        return dot




    def causfirst_fullconnected(self,basename,del_dup=True,dot=None):
        df = self.df
        self.del_dup = del_dup

        funclist = df.columns.to_list()

        edgelist = []
        boxnodelist = []
        invisedgelist = []
        sameranklist = []
        
        methodlist = df.index.to_list()
        methodlist = list(map(str, methodlist) )        
     

        for itime in range(df.shape[1]):
            methodlist = []
            applylist = []
            for imethod in range(df.shape[0]):
                cell1 = df.iloc[imethod,itime]
                if cell1 == cell1: # not nan
                    func1,method1 = self.get_func_method_1(cell1,func_prefix="apply_")
                    methodlist.append(method1)
                    func1,method1 = self.get_func_method_1(cell1,method_prefix="apply_")
                    applylist.append(method1)
                    
            funcp = funclist[itime]
            for method in methodlist:
                edgelist.append("{},{}".format(funcp,method))
                boxnodelist.append(method)
                
            #for method1,method2 in zip(methodlist[:-1],methodlist[1:]):
            #    invisedgelist.append("{},{}".format(method1,method2))
            sameranklist.append(",".join(methodlist))

            if itime>0:
                func1 = funclist[itime-1]
                for meth,ap in zip(methodlist,applylist):
                    edgelist.append("{},{}".format(meth,ap))
                    edgelist.append("{},{}".format(meth,func1))
                    invisedgelist.append("{},{}".format(func1,ap))
                    boxnodelist.append(meth)
                xlist = copy.deepcopy(applylist)
                xlist.append(func1)
                sameranklist.append(",".join(xlist))
                #invisedgelist.append(",".join(methodlist))

        
        self.edgelist = edgelist
        self.invisedgelist = invisedgelist
        self.boxnodelist = boxnodelist
        self.sameranklist = sameranklist
        
        
        self.drop_dup()
        if dot is  None:
            dot = Digraph(basename,filename=basename)
        dot = self.gen_dot(dot)

        return dot    

    def wayfirst(self,basename,del_dup=True,dot=None):
        df = self.df
        self.del_dup = del_dup

        edgelist = []
        boxnodelist = []
        invisedgelist = []
        sameranklist = []
 
        wayp = df.index.name
        cell1 = wayp
        funcp,methodp = self.get_func_method_1(cell1)
        methodlist = df.index.to_list()
        methodlist = list(map(str, methodlist) )
        
        methodstrlist = []
        for x in methodlist:
            if x==x:
                methodstrlist.append(self.method_prefix+x)
            
        
        for meth in methodstrlist:
            edgelist.append(",".join([funcp,meth]))  
            boxnodelist.append(meth)
        #invisedgelist.append(",".join(methodstrlist))
        sameranklist.append(",".join(methodstrlist))
        
        for imethod in range(df.shape[0]):
            methodlist = []
            applylist = []
            methodp = methodstrlist[imethod]
            elist = []
            for itime in range(df.shape[1]):
                cell1 = df.iloc[imethod,itime]
                if cell1!=cell1: 
                    continue
                _,func1 = self.get_func_method_1(cell1,method_prefix="apply_")
                _,meth1 = self.get_func_method_1(cell1,func_prefix="get_")
                edgelist.append(",".join([methodp,func1]))
                if False:
                    edgelist.append(",".join([func1,meth1]))
                    boxnodelist.append(meth1)
                elist.append(func1)
                
            invisedgelist.append(",".join(elist))
            sameranklist.append(",".join(elist))
            
        self.edgelist = edgelist
        self.invisedgelist = invisedgelist
        self.boxnodelist = boxnodelist
        self.sameranklist = sameranklist
        
        self.drop_dup()
        
        if dot is  None:
            dot = Digraph(basename,filename=basename)        
        
        dot = self.gen_dot(dot)
        
        return dot    


basename = "decisiontable"
#basename = "methofuncmatrix"

df0 = pd.read_csv(basename+".csv",index_col=[0])


# In[45]:


fdt = DecompositionTree(df0)    
dot = fdt.wayfirst("wayfirst_"+basename,del_dup=True)
dot.format="png"
dot.render(view=True)


# In[46]:


fdt = DecompositionTree(df0)    
dot = fdt.causfirst_fullconnected("causFull_"+basename,del_dup=True)
dot.format="png"
dot.render(view=True)


# In[47]:


fdt = DecompositionTree(df0)    
dot = fdt.funcfirst("funcfirst_"+basename,del_dup=True)
dot.format="png"
dot.render(view=True)


# In[48]:


fdt = DecompositionTree(df0)    
dot = fdt.causfirst_sparse("causSparse_"+basename,del_dup=True)
dot.format="png"
dot.render(view=True)


# In[ ]:





# In[ ]:




