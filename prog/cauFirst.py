#!/usr/bin/env python
# coding: utf-8

# 
#
#  (C) 2020 Hiori Kino
# 
# This software includes the work that is distributed in the Apache License 2.0
#
#

import os
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

        self.dotoption={"node_sequence_style":"invis", "nodelabel_length":15, 
             "apply_same_rank": False, "samerank": None, "connect_invis": True,
             "concentrate": True }

        if dotoption is not None:
           self.dotoption.update(dotoption)

        #print("init:dotoption",dotoption)
        
        self.nodelabel_length = self.dotoption["nodelabel_length"]
        
        self.nodetype = ["method","parts","function"] 
        self.linktype = ["is-a","part-of","FunctionFirst"]

        self.node_sequence_style = self.dotoption["node_sequence_style"]
        
        self.edgelist = []
        self.invisedgelist = []
        self.boxnodelist = []
        self.isanodelist = []
        self.sameranklist = []
        self.applynodelist = []

        self.cmdsameranklist =  None
        if self.dotoption["samerank"] is not None:
            self.cmdsameranklist = self.dotoption["samerank"]
            #print("cmdsameranklist",self.cmdsameranklist)

    def make_nodelabel(self,s):
        if self.nodelabel_length>5:
            v = [ s[i:i+self.nodelabel_length] for i in range(0,len(s),self.nodelabel_length) ]
            return "\n".join(v)
        else:
            return s
     
    def method_prefix(self,linktype=None):
        if linktype is None:
            linktype = "method"
        if linktype == "parts":
            return "method_toGet_"
        elif linktype == "method" or linktype == "direct":
            return ""
        elif linktype == "function":
            return "method_to_"
        else:
            print("method_prefix: unsupported",linktype)
            raise

    def func_prefix(self,linktype=None):
        if linktype is None:
            linktype ="parts"
        if linktype == "parts":
            return "get_"
        elif linktype == "method":
            return "get_outputOf_"
        elif linktype == "function" or linktype == "direct":
            return ""
        else:
            print("func_prefix: unsupported",linktype)
            raise 
            
    def applymethod_prefix(self,linktype=None):
        if linktype is None:
            linktype = "method"
        if linktype == "parts":
            return "apply_methodToGet_"
            #return "apply_"
        elif linktype == "method":
            return "apply_"
        elif linktype == "function":
            #return "apply_methodTo_"
            return "(apply)"
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
            self.isanodelist = list(set(self.isanodelist))
            self.sameranklist = list(set(self.sameranklist))

    def gen_tree(self,dottree,del_dup=True):
        self.drop_dup(del_dup)
        edgelist = self.edgelist
        invisedgelist = self.invisedgelist
        boxnodelist = self.boxnodelist
        isanodelist = self.isanodelist
        sameranklist = self.sameranklist
        cmdsameranklist = self.cmdsameranklist
        applynodelist = self.applynodelist

        apply_same_rank = self.dotoption["apply_same_rank"]
        #print("gen_tree: apply_same_rank",apply_same_rank)

        if cmdsameranklist is not None:
            for samerank in [cmdsameranklist]:
                s = samerank.split(",")
                with dottree.subgraph() as sub:
                    sub.attr(rank="same")
                    for x in s:
                        sub.node(x)
                for x in s:
                    dottree.node(x,style="solid,filled",fillcolor="darkslategray1")


        connect_invis = self.dotoption["connect_invis"]
        print("connect_invis",connect_invis)
        
        for edge in edgelist:
            s = edge.split(",")
            for x in s:
                dottree.node(x,label= self.make_nodelabel(x),shape="oval")
        for edge in edgelist:
            s = edge.split(",")
            for x0,x1 in zip(s[:-1],s[1:]):
                dottree.edge(x0,x1)
        if connect_invis:
            for invisedge in invisedgelist:
                s = invisedge.split(",")
                for x0,x1 in zip(s[:-1],s[1:]):
                    dottree.edge(x0,x1,style=self.node_sequence_style)
        for isanode in isanodelist:
            dottree.node(isanode,style="filled",bgcolor="gray")

        for boxnode in boxnodelist:
            dottree.node(boxnode,shape="box")
        for applynode in applynodelist:
            dottree.node(applynode,shape="octagon")
        if apply_same_rank:
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
            dottree.graph_attr["rankdir"] = "TB;"
            dottree.graph_attr["concentrate"] = str(self.dotoption["concetrate"])+";"

        dottree = self.gen_tree(dottree)
        return dottree
        

class workflowWay(DecompositionTree):
    def __init__(self,basename="wf",dotoption=None):
        super().__init__(basename,dotoption)

        #self.den_edgelist = []

        #self.excludenodelist = []

        self.wf_edgelist = []
        self.wf_objlist = []
        self.wf_methodlist = []
        self.wf_invisedgelist = []
        self.wf_sameranklist = []

        self.data = None

    def load(self,filename=None,data=None):
        if data is None and filename is not None:
            with open(filename) as f:
                data = yaml.safe_load(f)
            self.data = data
        elif filename is None and data is not None:
            self.data = data
        else:
            print("error: in load")
            raise

    def get_keyvalue(self,line,key):
        line = dict(line)
        if key in line.keys():
            value = line[key]
        else:
            value = None
        return value

    def check_names(self,g2):
        namelist = ["outputname","outputtype","methodname","methodtype"]
        try:
            g2 = dict(g2)
        except:
            print("failed to dict(g2),g2=",g2)
            raise
        for x in g2.keys():
            if x not in namelist:
                print("unknown keyword",x)
                print("group=",g2)
                print("keywordlist=",namelist)
                raise 

    def gen_names(self,g2):

        self.check_names(g2)

        complement = self.get_keyvalue(g2,"complement")

        if complement == "auto":

            nodename2 = self.get_keyvalue(g2,"outputname")
            methodname2 = self.get_keyvalue(g2,"methodname")
            functype2 = self.get_keyvalue(g2,"outputtype")
            methodtype2 = self.get_keyvalue(g2,"methodtype")
            if nodename2 is not None:
                funcname2 = self.func_prefix(functype2)+nodename2
            applymethodname2 = None

            if nodename2 is None and methodname2 is not None:
                nodename2 = "outputOf_to"+methodname2
                funcname2 = "gen_outputOfTo_"+methodname2                   
                nodetype2 = "auto"
            elif nodename2 is not None and methodname2 is None:
                methodname2 = "method_to_"+funcname2
                methodtype2 = "auto"

            applymethodname2 = self.applymethod_prefix("method")+methodname2

        else:

            nodename2 = self.get_keyvalue(g2,"outputname")
            functype2 = self.get_keyvalue(g2,"outputtype")
            rawmethodname2 = self.get_keyvalue(g2,"methodname")
            methodtype2 = self.get_keyvalue(g2,"methodtype")
            funcname2 = self.func_prefix(functype2)+nodename2
            applymethodname2 = None

            methodname2 = rawmethodname2
            if rawmethodname2 is not None:
                methodname2 = self.method_prefix(methodtype2)+rawmethodname2
                applymethodname2 = self.applymethod_prefix(methodtype2)+rawmethodname2

        return nodename2,funcname2,functype2,methodname2,methodtype2,applymethodname2
 

    def convert_from_workflow(self,wflist):
        wf = wflist["list"]

        grouplist = []
        for groupline in wf:
            grouplist.append( groupline["group"] )

        # node order
        for group1 in grouplist:
            funcname1list = []
            nodename1list = []
            methodname1list = []
            for g1 in group1:
                nodename1,funcname1,funtype1,methodname1,methodtype1,_ = self.gen_names(g1)

                funcname1list.append(funcname1)
                nodename1list.append(nodename1)
                if methodname1 is not None:
                    methodname1list.append(methodname1)
            if len(funcname1list)>1:
                self.invisedgelist.append(",".join(funcname1list))
                self.sameranklist.append(",".join(funcname1list))
            if len(methodname1list)>1:
                self.wf_invisedgelist.append(",".join(methodname1list))
                self.wf_sameranklist.append(",".join(methodname1list))

        for group1,group2 in zip(grouplist[:-1],grouplist[1:]):

            for g1 in group1:
                nodename1,funcname1,functype1,methodname1,methodtype1,_ = self.gen_names(g1)

                funcname1list.append(funcname1)

                for g2 in group2:

                    nodename2,funcname2,functype2,methodname2,methodtype2,applymethodname2 = self.gen_names(g2)

                    if methodname2 is not None:
                       self.edgelist.append(",".join([funcname2,methodname2]))
                       self.edgelist.append(",".join([methodname2,funcname1]))
                       self.edgelist.append(",".join([methodname2,applymethodname2]))
                       self.boxnodelist.append(methodname2) 
                       self.invisedgelist.append(",".join([funcname1,applymethodname2]))
                       self.sameranklist.append(",".join([funcname1,applymethodname2]))
                       self.applynodelist.append(applymethodname2)
                    if methodname1 is not None:
                       self.edgelist.append(",".join([funcname1,methodname1]))
                       self.boxnodelist.append(methodname1)


                    if methodname1 is not None and nodename1 is not None:
                       self.wf_edgelist.append(",".join([methodname1,nodename1]))
                    if methodname2 is not None and nodename1 is not None:
                       self.wf_edgelist.append(",".join([nodename1,methodname2]))
                    if methodname2 is not None and nodename2 is not None:
                       self.wf_edgelist.append(",".join([methodname2,nodename2]))

                    if methodname1 is not None:
                        self.wf_methodlist.append("{0},{{{0}|{1}}}".format(methodname1,methodtype1))
                    if methodname2 is not None:
                        self.wf_methodlist.append("{0},{{{0}|{1}}}".format(methodname2,methodtype2))
                    if nodename1 is not None:
                        self.wf_objlist.append("{0},{{{0}|{1}}}".format(nodename1,functype2))
                    if nodename2 is not None:
                        self.wf_objlist.append("{0},{{{0}|{1}}}".format(nodename2,functype2))

    def drop_wf_dup(self,del_dup=True):
        if del_dup:
            self.wf_edgelist = list(set(self.wf_edgelist))
            self.wf_invisedgelist = list(set(self.wf_invisedgelist))
            self.wf_objlist = list(set(self.wf_objlist))
            self.wf_methodlist = list(set(self.wf_methodlist))
            self.wf_sameranklist = list(set(self.wf_sameranklist))

    def create_workflow(self,dot=None):
        if dot is None:
            dot = graphiz(self.basename)
            dot.graph_attr["rankdir"] = "BT"

        self.drop_wf_dup()


        for edge in self.wf_edgelist:
            edge = edge.split(",")
            for edge1,edge2 in zip(edge[:-1],edge[1:]):
                dot.edge(edge1,edge2)
#        for node in self.boxnodelist:
#            dot.node(node,shape="record")
        invisstyle = self.dotoption["node_sequence_style"]
        for edge in self.wf_invisedgelist:
            edge = edge.split(",")
            for edge1,edge2 in zip(edge[:-1],edge[1:]):
                dot.edge(edge1,edge2,style=invisstyle)
        for node in self.wf_objlist:
            s = node.split(",")
            dot.node(s[0],shape="record",color="white",label=s[1]) 
        for node in self.wf_methodlist:
            s = node.split(",")
            dot.node(s[0],shape="record",label=s[1]) 
        for samerank in self.wf_sameranklist:
            s = samerank.split(",")
            with dot.subgraph() as sub:
                sub.attr(rank="same")
                for x in s:
                    sub.node(x)

        return dot 

    def linktree(self):
        data = self.data
        wf = data["workflow"]
        for wfblock in wf["block"]:
           self.convert_from_workflow(wfblock)

       
class taxologyWay(DecompositionTree):
    def __init__(self,basename="taxo",dotoption=None):

        super().__init__(basename,dotoption)

        self.den_edgelist = []

        self.excludenodelist = []
        self.data = None


    def load(self,filename=None,data=None):
        if filename is not None and data is None:
            with open(filename) as f:
                data = yaml.safe_load(f)
            self.data = data
        elif filename is None and data is not None:
            self.data = data
        else:
            print("erorr in load")
            raise


    def create_dendrogram(self,dot=None):
        den_edgelist = self.den_edgelist 
        if dot is None:
            dot = Digraph(self.basename)
            dot.graph_attr["rankdir"] = "TB"
        for den in den_edgelist:
            den0 = den[0]
            den1 = den[1]
            dot.edge(den0[0],den1[0])
            dot.node(den0[0],shape="record",label="{{{}|{}|{}}}".format(den0[0],den0[1],den0[2]))
            dot.node(den1[0],shape="record",label="{{{}|{}|{}}}".format(den1[0],den1[1],den1[2]))
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
        if plinkname is not None:
            pnodename = plinkname
            for linkline in linklist:
                #name = linkline["nodename"]
                name = self.get_keyvalue(linkline,"nodename")
                linktype = self.get_keyvalue(linkline,"linktype")
                link = self.get_keyvalue(linkline,"link")
                nodetype = self.get_keyvalue(linkline,"nodetype")
                self.den_edgelist.append([[pnodename,pnodetype,plinktype],
                                          [name,nodetype,linktype]])

        if plinkname is None:
            for linkline in linklist:
                name = self.get_keyvalue(linkline,"nodename")
                linktype = self.get_keyvalue(linkline,"linktype")
                link = self.get_keyvalue(linkline,"link")
                nodetype = self.get_keyvalue(linkline,"nodetype")
                self.gen_connection_link_link(link,linktype,name,nodetype)
        else:
            if plinktype == "part-of" or plinktype == "or" or plinktype is None:
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

                self.applynodelist.append(applyp)
                self.edgelist.append(",".join([methodp,applyp]))
                funcnamelist.append(applyp)
                self.invisedgelist.append(",".join(funcnamelist))
                self.sameranklist.append(",".join(funcnamelist))

            elif plinktype == "is-a" or plinktype == "xor" :

                namelist = []
                for linkline in linklist:
                    name = self.get_keyvalue(linkline,"nodename")
                    linktype = self.get_keyvalue(linkline,"linktype")
                    link = self.get_keyvalue(linkline,"link")
                    nodetype = self.get_keyvalue(linkline,"nodetype")

                    print(">",plinkname,plinktype,"->",name,nodetype,link,linktype)

                    no_mf = False


                    namelist.append(name)

                    # funcp->method1 edge
                    # method1 -> func1 edge
                    funcp = self.func_prefix(pnodetype) + plinkname
                    methodp = self.method_prefix(pnodetype) + plinkname
                    func1 = self.func_prefix(nodetype) + name
                    method1 = self.method_prefix(nodetype) + name

                    self.isanodelist.append(funcp)
                    self.edgelist.append(",".join([funcp,method1]))
                    print("edge:funcp->method1",[funcp,method1])
                    if linktype != "part-of":
                        self.edgelist.append(",".join([method1,func1]))
                        print("edge:method1->func1",[method1,func1])
                        
                    self.boxnodelist.append(method1)
                    self.excludenodelist.append(name)
              
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
        if "link" in list(data.keys()):
            #print("linktyp",linktype)
            #print(yaml.dump(data))
            self.gen_connection_link_link([data],linktype)


class FDTree(object):
    def __init__(self,basename = "caus", dottree=None,dotoption=None):
        self.dotoption = None
        if dotoption is None:
            #self.dotoption = {"node_sequence_style":"dotted", "nodelabel_length": 0, "apply_same_rank": False }
            self.dotoption = { "nodelabel_length": 15}
        else:
            self.dotoption = dotoption

        self.dottree = dottree
        if dottree is None:
            self.dottree = Digraph(basename)
            self.dottree.graph_attr["rankdir"] = "TB;"
            #self.dottree.graph_attr["concentrate"] = "true;"
            self.dottree.graph_attr["concentrate"] = str(self.dotoption["concentrate"])+";"
            self.dottree.edge_attr["len"] = "2.2"


    def apply(self,dataall,basename = None,make_png = True): 
        if basename is None:
            basename = "caus"

        dotoption = self.dotoption
        dottree = self.dottree

        #print("DFTree:dotoption",dotoption)

        # options,  fix them now
        no_wf = True
        no_taxo = True

        for key in dataall:
            data = dataall[key]

            if key == "workflow":
                wf = workflowWay(dotoption=dotoption)
                wf.load(data={"workflow":data})
                wf.linktree()
                dottree = wf.create_tree(dottree)

                if not no_wf :
                    dotwf = Digraph(basename)
                    dotwf.graph_attr["rankdir"] = "BT"
                    dotwf = wf.create_workflow(dotwf)
                    dotwf.format = "png"
                    dotwf.render(view=False)
 
            elif key == "linkset":
                taxo = taxologyWay(dotoption=dotoption)

                for ataxo in data["block"]:
                    taxo.load(data=ataxo)
                    taxo.linktree()
                    dottree = taxo.create_tree(dottree)

                if not no_taxo:
                    dottaxo = Digraph(basename)
                    dottaxo.graph_attr["rankdir"] = "TB"
                    dottaxo = taxo.create_dendrogram(dottaxo)
                    dottaxo.format = "png"
                    dottaxo.render(view=False)

        if make_png:
            dottree.format="png"
            dottree.render(view=False)
            print("png is made.")

        return dottree

    def apply_files(self,namelist):

        dotoption = self.dotoption
        dottree = self.dottree

        for filename in namelist:

            basename,ext = os.path.splitext(filename)
            #ext = ext[1:]

            with open(filename) as f:
                dataall = yaml.safe_load(f)

            self.apply(dataall,make_png = False)

        if True:
            dottree.format="png"
            dottree.render(view=False)
            print("png is made.")

      
if __name__ == "__main__":
    import sys 
    import os
    import argparse

    def parse_cmd_option():
        parser = argparse.ArgumentParser()
        parser.add_argument("filenames",nargs="*")
        parser.add_argument("--no_wf",action="store_true")
        parser.add_argument("--no_taxo",action="store_true")
        parser.add_argument("--no_connect_invis",dest="connect_invis",action="store_true")
        parser.add_argument("--no_concentrate",dest="concentrate",action="store_false")
        parser.add_argument("--samerank",default=None)


        cmdopt = parser.parse_args()

        #return cmdopt.filenames
        return cmdopt

    def doit_each(namelist):
        dottree = Digraph("caus")
        dottree.graph_attr["rankdir"] = "TB"
        dottree.graph_attr["concentrate"] = str(self.dotoption["concetrate"])+";"

        for filename in namelist:

            basename,ext = os.path.splitext(filename)
            #ext = ext[1:]

            with open(filename) as f:
                dataall = yaml.safe_load(f)

            fdtree = FDTree(dottree,basename)
            dottree = fdtree.apply(dataall,make_png=False)
       
        dottree.format="png"
        dottree.render(view=False)
        print("done")

    # start 

    cmdopt = parse_cmd_option()
    print(cmdopt)
    namelist = cmdopt.filenames
                    
    if len(namelist)==0:
        sys.exit(1)

    doit = "all"

    if doit == "each":
        doit_each(namelist)

    elif doit == "all":
        
        fdtree = FDTree(dotoption=cmdopt.__dict__)
        dottree = fdtree.apply_files(namelist)

    #end 


