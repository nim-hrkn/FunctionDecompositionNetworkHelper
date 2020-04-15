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

    def __init__(self,basename = "caus",dotoption=None):
        if basename is None:
            basename = "caus"
        self.basename = basename

        self.dotoption={"node_sequence_style":"invis", "nodelabel_length":15}
        if dotoption is not None:
           self.dotoption.update(dotoption)
        
        self.nodelabel_length = self.dotoption["nodelabel_length"]
        
        self.nodetype = ["method","parts","function"] 
        self.linktype = ["IsA","PartOf","FunctionFirst"]

        self.node_sequence_style = self.dotoption["node_sequence_style"]
        
        self.edgelist = []
        self.invisedgelist = []
        self.boxnodelist = []
        self.sameranklist = []

    def make_nodelabel(self,s):
        if self.nodelabel_length>0:
            v = [ s[i:i+self.nodelabel_length] for i in range(0,len(s),self.nodelabel_length) ]
            return "\n".join(v)
        else:
            return v
     
    def method_prefix(self,linktype=None):
        if linktype is None:
            linktype = "method"
        if linktype == "parts":
            return "method_toGet_"
        elif linktype == "method":
            return ""
        elif linktype == "function":
            return "method_to_"
        else:
            print("method_prefix: unsupported",linktype)
            raise

    def func_prefix(self,linktype=None):
        if linktype is None:
            linktype ="parts"
        if linktype=="parts":
            return "get_"
        elif linktype == "method":
            return "get_outputOf_"
        elif linktype=="function":
            return ""
        else:
            print("func_prefix: unsupported",linktype)
            raise 
            
    def applymethod_prefix(self,linktype=None):
        if linktype is None:
            linktype = "method"
        if linktype=="parts":
            return "apply_methodToGet_"
        elif linktype == "method":
            return "apply_"
        elif linktype=="function":
            return "apply_methodTo_"
        else:
            print("applymethod_prefix: unsupported",linktype)
            raise
       
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
            for x in s:
                dottree.node(x,label= self.make_nodelabel(x))
        for edge in edgelist:
            s = edge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dottree.edge(x0,x1)
        for invisedge in invisedgelist:
            s = invisedge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dottree.edge(x0,x1,style=self.node_sequence_style)
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
            dottree.graph_attr["rankdir"] = "TB"

        dottree = self.gen_tree(dottree)
        return dottree
        

class workflowWay(DecompositionTree):
    def __init__(self,basename="taxo",dotoption=None):
        print("workflowWay")
        super().__init__(basename,dotoption)

        self.den_edgelist = []

        self.excludenodelist = []
        self.data = None

    def load(self,filename):
        data = None
        with open(filename) as f:
            data = yaml.safe_load(f)
        self.data = data
        print(data)

    def get_keyvalue(self,line,key):
        if key in line.keys():
            value = line[key]
        else:
            value = None
        return value

    def convert_workflow(self,wf):
        grouplist = []
        for groupline in wf:
            grouplist.append( groupline["group"] )

        # node order
        for group1 in grouplist:
            funcname1list = []
            for g1 in group1:
                nodename1 = self.get_keyvalue(g1,"funcname")
                functype1 = self.get_keyvalue(g1,"functype")
                funcname1 = self.func_prefix(functype1)+nodename1
                funcname1list.append(funcname1)
            if len(funcname1list)>1:
                print(">invis",funcname1list)
                self.invisedgelist.append(",".join(funcname1list))
                self.sameranklist.append(",".join(funcname1list))

        for group1,group2 in zip(grouplist[:-1],grouplist[1:]):
            print("g1",group1)
            print("g2",group2)

            funcname1list = []
            for g1 in group1:
                nodename1 = self.get_keyvalue(g1,"funcname")
                functype1 = self.get_keyvalue(g1,"functype")
                funcname1 = self.func_prefix(functype1)+nodename1
            if len(funcname1list)>1:
                self.invisedgelist.append(",".join(funcname1list))
            funcname2list = []
            for g2 in group2:
                nodename2 = self.get_keyvalue(g2,"funcname")
                functype2 = self.get_keyvalue(g2,"functype")
                funcname2 = self.func_prefix(functype2)+nodename2
            if len(funcname2list)>1:
                self.invisedgelist.append(",".join(funcname2list))

            for g1 in group1:
                nodename1 = self.get_keyvalue(g1,"funcname")
                functype1 = self.get_keyvalue(g1,"functype")
                methodname1 = self.get_keyvalue(g1,"methodname")
                methodtype1 = self.get_keyvalue(g1,"methodtype")
                funcname1 = self.func_prefix(functype1)+nodename1

                funcname1list.append(funcname1)

                if methodname1 is not None:
                    methodname1 = self.method_prefix(methodtype1)+methodname1

                for g2 in group2:
                    nodename2 = self.get_keyvalue(g2,"funcname")
                    functype2 = self.get_keyvalue(g2,"functype")
                    methodname2 = self.get_keyvalue(g2,"methodname")
                    methodtype2 = self.get_keyvalue(g2,"methodtype")
                    funcname2 = self.func_prefix(functype2)+nodename2

                    print("apply",functype2,methodname2)
                    applymethodname2 = self.applymethod_prefix(functype2)+methodname2

                    if methodname2 is not None:
                        methodname2 = self.method_prefix(methodtype2)+methodname2

                    if methodname2 is not None:
                       self.edgelist.append(",".join([funcname2,methodname2]))
                       self.edgelist.append(",".join([methodname2,funcname1]))
                       self.edgelist.append(",".join([methodname2,applymethodname2]))
                       self.boxnodelist.append(methodname2) 
                       self.invisedgelist.append(",".join([funcname1,applymethodname2]))
                       self.sameranklist.append(",".join([funcname1,applymethodname2]))
                    if methodname1 is not None:
                       self.edgelist.append(",".join([funcname1,methodname1]))
                       self.boxnodelist.append(methodname1)

                    print("> [{}]({})-{}({})-".format(methodname1,methodtype1,funcname1,functype1),)
                    print("> [{}]({})-{}({})".format(methodname2,methodtype2,funcname2,functype2))
                    print()


    def gen_dendrogram(self,workflowlist):
        for wf in workflowlist:
            self.convert_workflow(wf["workflow"])

    def linktree(self):
        data = self.data
        self.gen_dendrogram(data["workflow"])


class taxologyWay(DecompositionTree):
    def __init__(self,basename="taxo",dotoption=None):

        super().__init__(basename,dotoption)

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
        if dot is None:
            dot = Digraph(self.basename)
            dot.graph_attr["rankdir"] = "TB"
        for den in den_edgelist:
            dot.edge(den[0],den[1])
            dot.node(den[0],shape="box")
            dot.node(den[1],shape="box")
        return dot

    def get_keyvalue(self,line,key):
        if key in line.keys():
            value = line[key]
        else:
            value = None
        return value

    def gen_connection_link_link(self,linklist,plinktype=None,plinkname=None,pnodetype=None):
        if linklist is None:
            return 
        print(">>>",plinkname,pnodetype,plinktype)
        if plinkname is not None:
            pnodename = plinkname
            for linkline in linklist:
                name = linkline["nodename"]
                self.den_edgelist.append([pnodename,name])

        if plinkname is None:
            for linkline in linklist:
                name = self.get_keyvalue(linkline,"nodename")
                linktype = self.get_keyvalue(linkline,"linktype")
                link = self.get_keyvalue(linkline,"link")
                nodetype = self.get_keyvalue(linkline,"nodetype")
                self.gen_connection_link_link(link,linktype,name,nodetype)
        else:
            if plinktype == "PartOf" or plinktype is None:
                funcnamelist = []
                for linkline in linklist:
                    name = self.get_keyvalue(linkline,"nodename")
                    linktype = self.get_keyvalue(linkline,"linktype")
                    link = self.get_keyvalue(linkline,"link")
                    nodetype = self.get_keyvalue(linkline,"nodetype")
       
                    #funcp->methodp edge
                    funcp = self.func_prefix(pnodetype) + plinkname
                    methodp = self.method_prefix(pnodetype) + plinkname 

                    if plinkname not in self.excludenodelist:
                        self.edgelist.append(",".join([funcp,methodp]) ) 
                    self.boxnodelist.append(methodp)

                    #methodp->func edge
                    func1 = self.func_prefix(nodetype)+ name
                    self.edgelist.append(",".join([methodp,func1]))

                    funcnamelist.append(func1)
                  
                    self.gen_connection_link_link(link,linktype,name,nodetype)

                applyp = self.applymethod_prefix(pnodetype) + plinkname
                print(">",plinkname, plinktype,pnodetype,applyp)

                self.edgelist.append(",".join([methodp,applyp]))
                funcnamelist.append(applyp)
                self.invisedgelist.append(",".join(funcnamelist))
                self.sameranklist.append(",".join(funcnamelist))

            elif plinktype == "IsA":

                namelist = []
                for linkline in linklist:
                    name = self.get_keyvalue(linkline,"nodename")
                    linktype = self.get_keyvalue(linkline,"linktype")
                    link = self.get_keyvalue(linkline,"link")
                    nodetype = self.get_keyvalue(linkline,"nodetype")

                    print(">>",pnodename,plinktype,pnodetype,":",name,nodetype,linktype)
                    print(">",link)


                    namelist.append(name)

                    #funcp->methodp edge
                    funcp = self.func_prefix(pnodetype) + plinkname
                    methodp = self.method_prefix(pnodetype) + plinkname
                    func1 = self.func_prefix(nodetype) + name
                    method1 = self.method_prefix(nodetype) + name

                    if link is None: 
                        self.edgelist.append(",".join([funcp,method1]))
                        self.boxnodelist.append(method1)
                    else:
                        self.edgelist.append(",".join([funcp,methodp]))
                        self.boxnodelist.append(methodp)
                        self.edgelist.append(",".join([methodp,func1]))
                  
                    self.gen_connection_link_link(link,linktype,name,nodetype)

            elif plinktype == "FunctionFirst":
                namelist = []
                for linkline1,linkline2 in zip(linklist[:-1],linklist[1:]):

                    name1 = self.get_keyvalue(linkline1,"nodename")
                    linktype1 = self.get_keyvalue(linkline1,"linktype")
                    link1 = self.get_keyvalue(linkline1,"link")
                    nodetype1 = self.get_keyvalue(linkline1,"nodetype")
                    
                    name2 = self.get_keyvalue(linkline2,"nodename")
                    linktype2 = self.get_keyvalue(linkline2,"linktype")
                    link2 = self.get_keyvalue(linkline2,"link")
                    nodetype2 = self.get_keyvalue(linkline2,"nodetype")

                    funcp = self.func_prefix(pnodetype) + plinkname
                    methodp = self.method_prefix(pnodetype) + plinkname
                    func1 = self.func_prefix(nodetype1) + name1
                    method1 = self.method_prefix(nodetype1) + name1
                    func2 = self.func_prefix(nodetype2) + name2
                    method2 = self.method_prefix(nodetype2) + name2
                    apply2 = self.applymethod_prefix(nodetype2) + name2

                    # generate links
                    self.edgelist.append(",".join([func2,method2]))
                    self.boxnodelist.append(method2)
                    self.edgelist.append(",".join([method2,func1]))
                    self.edgelist.append(",".join([method2,apply2]))
                    self.invisedgelist.append(",".join([func1,apply2]))
                    self.sameranklist.append(",".join([func1,apply2]))

                    self.gen_connection_link_link(link1,linktype1,name1,nodetype1)
                    self.gen_connection_link_link(link2,linktype2,name2,nodetype2)

            else:
                print("not supported, linktype=",plinktype)
                raise

                    
    def linktree(self):
        data = self.data
        linktype = self.get_keyvalue(data,"linktype")
        self.gen_connection_link_link(data["link"],linktype)

       

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
            func_prefix = self.func_prefix()
        cell1 = str(cell1)
        if cell1.find(":")<0:
            output1 = cell1
            way1 = cell1
        else:
            way1,output1 = cell1.split(":")
            if way1 is None:
                way1 = output1
        if method_prefix is None:
            method_prefix = self.method_prefix()
                    
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
            funcp = self.func_prefix()+output2
        else:
            funcp = None
        if len(wayp)>0:
            methodp = self.method_prefix()+wayp
        else:
            methodp = None
        if len(output1)>0:
            func1 = self.func_prefix()+output1
        else:
            func1 = None
        if len(wayp)>0:
            func2 = self.applymethod_prefix()+wayp    
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
            funcp = self.func_prefix()+output2
        else:
            funcp = None
        if len(wayp)>0:
            methodp = self.method_prefix()+wayp
        else:
            methodp = NOne
        if len(output0)>0:
            func0 = self.func_prefix()+output0
        else:
            func0 = None
        if len(output1)>0:
            func1 = self.func_prefix()+output1
        else:
            func1 = None
        if len(wayp)>0:
            func2 = self.applymethod_prefix()+wayp    
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
        return dottree 
    
    def nodes2funcs(self,nodes):
        funcs = []
        for node in nodes:
            funcs.append(self.func_prefix()+node)
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
                    
    if len(namelist)==0:
        sys.exit(1)

    dotoption = {"node_sequence_style":"dotted"}

    dottree = Digraph("caus")
    dottree.graph_attr["rankdir"] = "TB"

    for filename in namelist:

        basename,ext = os.path.splitext(filename)
        ext = ext[1:]

        with open(filename) as f:
            data = yaml.safe_load(f)
        print(list(data.keys()))
        if "workflow" in data.keys():
            filetype = "wf"
        elif "link" in data.keys():
            filetype = "taxo"
        else:
            print("format not supported in",filename)
            raise

        if ext in ["yml"]:
            if filetype == "wf":
                wf = workflowWay(dotoption=dotoption)
                wf.load(filename)
                wf.linktree()
                dottree = wf.create_tree(dottree)

            elif filetype == "taxo":
                taxo = taxologyWay(dotoption=dotoption)
                taxo.load(filename)
                taxo.linktree()
                dottree = taxo.create_tree(dottree)
    
    dottree.format="png"
    dottree.render(view=True)
    print("done")


