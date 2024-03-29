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
from graphviz import Digraph, Graph
import yaml


class DecompositionTree(object):
    """functional decomposition tree basic class
    """

    def __init__(self, basename="caus", dotoption=None):
        """initialize class

        Parameters
        ----------
        basenane: string
            name of the Digraph
        dotoption: dict
            options to the Digraph

        Returns
        -------
        None
        """
        if basename is None:
            basename = "caus"
        self.basename = basename

        self.dotoption = {"node_sequence_style": "invis",
                          "nodelabel_length": 15,
                          "apply_same_rank":  False,
                          "samerank": None, "connect_invis": True,
                          "concentrate": True}

        if dotoption is not None:
            self.dotoption.update(dotoption)

        self.nodelabel_length = self.dotoption["nodelabel_length"]

        self.nodetype = ["method", "parts", "function"]
        self.linktype = ["is-a", "part-of", "FunctionFirst"]

        self.node_sequence_style = self.dotoption["node_sequence_style"]

        self.edgelist = []
        self.invisedgelist = []
        self.boxnodelist = []
        self.isanodelist = []
        self.isaboxnodelist = []
        self.sameranklist = []
        self.applynodelist = []

        self.cmdsameranklist = None
        if self.dotoption["samerank"] is not None:
            self.cmdsameranklist = self.dotoption["samerank"]

    def make_nodelabel(self, s):
        """make label string of the node

        Parameters
        ----------
        s : string
            fold the string by 5

        Returns
        -------
        folded string by new lines
        """
        if self.nodelabel_length > 5:
            v = [s[i:i+self.nodelabel_length]
                 for i in range(0, len(s), self.nodelabel_length)]
            return "\n".join(v)
        else:
            return s

    def method_prefix(self, linktype=None):
        """add prefix of method according to linktype

        Parameters
        ----------
        linktype: string\
            a type of link, which are method, parts, direct, function

        Returns
        -------
        prefix for linktype: string
        """
        if linktype is None:
            linktype = "method"
        if linktype == "parts":
            return "Way_toGet_"
        elif linktype == "method" or linktype == "direct":
            return ""
        elif linktype == "function":
            return "Way_to_"
        else:
            print("method_prefix: unsupported", linktype)
            raise

    def func_prefix(self, linktype=None):
        """add prefix of function accoring to linktype

        Parameters
        ----------
        linktype: string
            a type of function, which are parts, method, direct, function

        Returns
        -------
        prefix for linktype: string
        """
        if linktype is None:
            linktype = "parts"
        if linktype == "parts":
            return "Obtain "
        elif linktype == "method":
            return "Obtain outputOf "
        elif linktype == "function" or linktype == "direct":
            return ""
        else:
            print("func_prefix: unsupported", linktype)
            raise

    def applyfunction_prefix(self, linktype=None):
        """add prefix of applyfunction accoring to linktype

        Parameters
        ----------
        linktype: string
            a type of function, which are parts, method, direct, function

        Returns
        -------
        prefix for linktype: string
        """
        if linktype is None:
            linktype = "method"
        if linktype == "parts":
            return "Apply methodToGet "
        elif linktype == "method":
            return "Apply "
        elif linktype == "function":
            return "(Apply)"
        else:
            print("applyfunction_prefix: unsupported", linktype)
            raise

    def check_extension(self, name, ext=None):
        """return extension of the filename with os.path.splitext()

        Parameters
        ----------
        name: filename

        Returns
        -------
        file extension
        """
        if ext is None:
            # check file extension
            basename, ext = os.path.splitext(name)
            ext = ext[1:]  # delete the first dottree
        return ext

    def drop_dup(self, del_dup):
        """delete duplicated elements in the dot list

        Parameters
        ----------
        del_dup: boolean
            delete  duplicated elements if True

        Returns
        -------
        None
        """
        if del_dup:
            self.edgelist = list(set(self.edgelist))
            self.invisedgelist = list(set(self.invisedgelist))
            self.boxnodelist = list(set(self.boxnodelist))
            self.isanodelist = list(set(self.isanodelist))
            self.sameranklist = list(set(self.sameranklist))

    def gen_tree(self, dottree, del_dup=True):
        """generate dot object from nodes and edges

        Parameters
        ----------
        dottree: Digraph

        del_dup: boolean
            delete duplicated elements if True

        Returns
        -------
        dottree
        """
        self.drop_dup(del_dup)
        edgelist = self.edgelist
        invisedgelist = self.invisedgelist
        boxnodelist = self.boxnodelist
        isanodelist = self.isanodelist
        isaboxnodelist = self.isaboxnodelist
        sameranklist = self.sameranklist
        cmdsameranklist = self.cmdsameranklist
        applynodelist = self.applynodelist

        apply_same_rank = self.dotoption["apply_same_rank"]

        if cmdsameranklist is not None:
            for samerank in [cmdsameranklist]:
                s = samerank.split(",")
                with dottree.subgraph() as sub:
                    sub.attr(rank="same")
                    for x in s:
                        sub.node(x)
                for x in s:
                    dottree.node(x, style="solid,filled",
                                 fillcolor="darkslategray1")

        connect_invis = self.dotoption["connect_invis"]
        print("connect_invis", connect_invis)

        for edge in edgelist:
            s = edge.split(",")
            for x in s:
                dottree.node(x, label=self.make_nodelabel(x), shape="oval")
        for edge in edgelist:
            s = edge.split(",")
            for x0, x1 in zip(s[:-1], s[1:]):
                dottree.edge(x0, x1)
        if connect_invis:
            for invisedge in invisedgelist:
                s = invisedge.split(",")
                for x0, x1 in zip(s[:-1], s[1:]):
                    dottree.edge(x0, x1, style=self.node_sequence_style)
        #for isanode in isanodelist:
        #    dottree.node(isanode, style="filled", bgcolor="gray")

        for boxnode in boxnodelist:
            if boxnode in isaboxnodelist:
                dottree.node(boxnode, shape="box", fillcolor="gray", style="filled")
            else:
                dottree.node(boxnode, shape="box")
        for applynode in applynodelist:
            dottree.node(applynode, shape="hexagon")
        if apply_same_rank:
            for samerank in sameranklist:
                s = samerank.split(",")
                with dottree.subgraph() as sub:
                    sub.attr(rank="same")
                    for x in s:
                        sub.node(x)

        return dottree

    def create_tree(self, dottree=None):
        """create dot tree

        Parameters
        ----------
        dottree: None of Digraph object
            create new Digraph object if dottree if None

        Returns
        -------
        Digraph object
        """
        if dottree is None:
            dottree = Digraph(self.basename)
            dottree.graph_attr["rankdir"] = "TB;"
            dottree.graph_attr["slines"] = "line;"
            dottree.graph_attr["concentrate"] =\
                str(self.dotoption["concetrate"])+";"

        dottree = self.gen_tree(dottree)
        return dottree


class workflowWay(DecompositionTree):
    """generate Decompositon Tree from flowchart
    """

    def __init__(self, basename="wf", dotoption=None):
        """initialize workflowWay class

        Parameters
        ----------
        basename: string
            name of Digraph

        dotoption: dict
            Digraph options
        """
        super().__init__(basename, dotoption)

        self.wf_edgelist = []
        self.wf_objlist = []
        self.wf_methodlist = []
        self.wf_invisedgelist = []
        self.wf_sameranklist = []

        self.data = None

    def load(self, filename=None, data=None):
        """load YML file or use data

        Parameters
        ----------
        filename: string or None
            load YAML if filename is not None
        data: yaml data or None
            use data if data is not NOne
        Returns
        -------
        None
        """
        if data is None and filename is not None:
            with open(filename) as f:
                data = yaml.safe_load(f)
            self.data = data
        elif filename is None and data is not None:
            self.data = data
        else:
            print("error: in load")
            raise

    def get_keyvalue(self, line, key):
        """get the value of the key in dict

        Parameters
        ----------
        line: dict
            dict to find the key

        Returns
        -------
        value of the key or None
        """
        line = dict(line)
        if key in line.keys():
            value = line[key]
        else:
            value = None
        return value

    def check_names(self, g2):
        """check whether names are correct or not

        Parameters
        ----------
        g2: dict or json
            check whether keys of the dict is among namelist in the code.

        Returns
        -------
        None
        """
        namelist = ["outputname", "outputtype", "wayname", "waytype",
                    "applywayname", "applywaytype"]
        try:
            g2 = dict(g2)
        except:
            print("failed to dict(g2),g2=", g2)
            raise
        for x in g2.keys():
            if x not in namelist:
                print("unknown keyword", x)
                print("group=", g2)
                print("keywordlist=", namelist)
                raise

    def gen_names(self, g2):
        """generate applipriate names from dict depending on method, function, ...

        Parameters
        ----------
        g2: dict
            dict information of the node-method-node

        Returns
        -------
        names: a list of string
        """

        self.check_names(g2)

        complement = self.get_keyvalue(g2, "complement")

        if complement == "auto":

            nodename2 = self.get_keyvalue(g2, "outputname")
            wayname2 = self.get_keyvalue(g2, "wayname")
            functype2 = self.get_keyvalue(g2, "outputtype")
            waytype2 = self.get_keyvalue(g2, "waytype")
            if nodename2 is not None:
                funcname2 = self.func_prefix(functype2)+nodename2
            applyfunctionname2 = None

            if nodename2 is None and wayname2 is not None:
                nodename2 = "outputOf_to"+wayname2
                funcname2 = "gen_outputOfTo_"+wayname2
                # nodetype2 = "auto"
            elif nodename2 is not None and wayname2 is None:
                wayname2 = "method_to_"+funcname2
                waytype2 = "auto"

            applyfunctionname2 = self.applyfunction_prefix("method") + wayname2

            rawapplywayname2 = self.func_prefix(g2, "applywayname")
            applywayname2 = rawapplywayname2
            applywaytype2 = self.func_prefix(g2, "applywaytype")
            if rawapplywayname2 is not None:
                applywayname2 = self.method_prefix(applywaytype2) + rawapplywayname2

        else:

            nodename2 = self.get_keyvalue(g2, "outputname")
            functype2 = self.get_keyvalue(g2, "outputtype")
            rawwayname2 = self.get_keyvalue(g2, "wayname")
            waytype2 = self.get_keyvalue(g2, "waytype")
            funcname2 = self.func_prefix(functype2)+nodename2
            applyfunctionname2 = None

            wayname2 = rawwayname2
            if rawwayname2 is not None:
                wayname2 = self.method_prefix(waytype2)+rawwayname2
                applyfunctionname2 = self.applyfunction_prefix(waytype2) + rawwayname2

            rawapplywayname2 = self.get_keyvalue(g2, "applywayname")
            applywayname2 = rawapplywayname2
            applywaytype2 = self.get_keyvalue(g2, "applywaytype")
            if rawapplywayname2 is not None:
                applywayname2 = self.method_prefix(applywaytype2) + rawapplywayname2

        return nodename2, funcname2, functype2, wayname2, waytype2, applyfunctionname2, applywayname2

    def convert_from_workflow(self, wflist):
        """convert from workflow list to workflow diagram

        Parameters
        ----------
        wflist: a list of flowchart

        Returns
        -------
        None
        """
        wf = wflist["list"]

        grouplist = []
        for groupline in wf:
            grouplist.append(groupline["group"])

        # node order
        for group1 in grouplist:
            funcname1list = []
            nodename1list = []
            wayname1list = []
            for g1 in group1:
                nodename1, funcname1, funtype1,\
                    wayname1, waytype1, _, _ = self.gen_names(g1)

                funcname1list.append(funcname1)
                nodename1list.append(nodename1)
                if wayname1 is not None:
                    wayname1list.append(wayname1)
            if len(funcname1list) > 1:
                self.invisedgelist.append(",".join(funcname1list))
                self.sameranklist.append(",".join(funcname1list))
            if len(wayname1list) > 1:
                self.wf_invisedgelist.append(",".join(wayname1list))
                self.wf_sameranklist.append(",".join(wayname1list))

        for group1, group2 in zip(grouplist[:-1], grouplist[1:]):

            for g1 in group1:
                nodename1, funcname1,\
                    functype1, wayname1,\
                    waytype1, _, _ = self.gen_names(g1)

                funcname1list.append(funcname1)

                for g2 in group2:

                    nodename2, funcname2,\
                        functype2, wayname2,\
                        waytype2, applyfunctionname2,\
                        applywayname2 = self.gen_names(g2)

                    if wayname2 is not None:
                        self.edgelist.append(",".join([funcname2,
                                                       wayname2]))
                        self.edgelist.append(",".join([wayname2,
                                                       funcname1]))
                        self.edgelist.append(",".join([wayname2,
                                                       applyfunctionname2]))
                        self.boxnodelist.append(wayname2)
                        self.invisedgelist.append(",".join([funcname1,
                                                            applyfunctionname2]))
                        self.sameranklist.append(",".join([funcname1,
                                                           applyfunctionname2]))
                        self.applynodelist.append(applyfunctionname2)
                        if applywayname2 is not None:
                            self.edgelist.append(",".join([applyfunctionname2,
                                                           applywayname2]))
                            self.boxnodelist.append(applywayname2)
                    if wayname1 is not None:
                        self.edgelist.append(",".join([funcname1,
                                                       wayname1]))
                        self.boxnodelist.append(wayname1)

                    if wayname1 is not None and nodename1 is not None:
                        self.wf_edgelist.append(",".join([wayname1,
                                                          nodename1]))
                    if wayname2 is not None and nodename1 is not None:
                        self.wf_edgelist.append(",".join([nodename1,
                                                          wayname2]))
                    if wayname2 is not None and nodename2 is not None:
                        self.wf_edgelist.append(",".join([wayname2,
                                                          nodename2]))

                    if wayname1 is not None:
                        self.wf_methodlist.append("{0},{{{0}|{1}}}".format(wayname1, waytype1))
                    if wayname2 is not None:
                        self.wf_methodlist.append("{0},{{{0}|{1}}}".format(wayname2, waytype2))
                    if nodename1 is not None:
                        self.wf_objlist.append("{0},{{{0}|{1}}}".format(nodename1, functype2))
                    if nodename2 is not None:
                        self.wf_objlist.append("{0},{{{0}|{1}}}".format(nodename2, functype2))

    def drop_wf_dup(self, del_dup=True):
        """delete duplicated elements in the list

        Parameters
        ----------
        del_dup: boolean

        Returns
        -------
        None
        """
        if del_dup:
            self.wf_edgelist = list(set(self.wf_edgelist))
            self.wf_invisedgelist = list(set(self.wf_invisedgelist))
            self.wf_objlist = list(set(self.wf_objlist))
            self.wf_methodlist = list(set(self.wf_methodlist))
            self.wf_sameranklist = list(set(self.wf_sameranklist))

    def fix_dotlabel(self, s):
        """fix label for Digraph

        Parameters
        ----------
        s: string

        Returns
        -------
        < or > are placed by \\< or \\>
        """
        s = s.replace("<", "\\<")
        s = s.replace(">", "\\>")
        return s

    def create_workflow(self, dot=None):
        """create workflowWay

        Parameters
        ----------
        dot: Digraph object or None
            created if it is None

        Returns
        -------
        DIgraph object

        """
        if dot is None:
            dot = Digraph(self.basename)
            dot.graph_attr["rankdir"] = "BT"
            dot.graph_attr["splines"] = "line"

        self.drop_wf_dup()

        for edge in self.wf_edgelist:
            edge = edge.split(",")
            for edge1, edge2 in zip(edge[:-1], edge[1:]):
                dot.edge(edge1, edge2)
#        for node in self.boxnodelist:
#            dot.node(node,shape="record")
        invisstyle = self.dotoption["node_sequence_style"]
        for edge in self.wf_invisedgelist:
            edge = edge.split(",")
            for edge1, edge2 in zip(edge[:-1], edge[1:]):
                dot.edge(edge1, edge2, style=invisstyle)
        for node in self.wf_objlist:
            s = node.split(",")
            dot.node(s[0], shape="record", color="white", label=self.fix_dotlabel(s[1]))
        for node in self.wf_methodlist:
            s = node.split(",")
            dot.node(s[0], shape="record", label=self.fix_dotlabel(s[1]))
        for samerank in self.wf_sameranklist:
            s = samerank.split(",")
            with dot.subgraph() as sub:
                sub.attr(rank="same")
                for x in s:
                    sub.node(x)

        return dot

    def linktree(self):
        """make decompositon tree from flowchart

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        data = self.data
        wf = data["workflow"]
        for wfblock in wf["block"]:
            self.convert_from_workflow(wfblock)


class taxologyWay(DecompositionTree):
    """make is-a, part-of diagram
    """

    def __init__(self, basename="taxo", dotoption=None):

        super().__init__(basename, dotoption)

        self.den_edgelist = []

        self.excludenodelist = []
        self.data = None

    def load(self, filename=None, data=None):
        """load filename or use dataall

        Parameters
        ----------
        filename: filename of json or None
            read filename if it is not None

        data: dict

        Returns
        -------
        None
        """
        print("---taxology load",filename,data)
        if filename is not None and data is None:
            with open(filename) as f:
                data = yaml.safe_load(f)
            self.data = data
            print("debug")
            print(data)
            
        elif filename is None and data is not None:
            self.data = data
        else:
            print("erorr in load")
            raise

    def create_dendrogram(self, dot=None):
        """create dendrogram diagram

        Parameters
        ----------
        dot: Digraph object or None
            create Digraph if it is None

        Returns
        -------
        Digraph object
        """
        den_edgelist = self.den_edgelist
        if dot is None:
            dot = Digraph(self.basename)
            dot.graph_attr["rankdir"] = "TB"
            dot.graph_attr["splines"] = "line"
        for den in den_edgelist:
            den0 = den[0]
            den1 = den[1]
            dot.edge(den0[0], den1[0])
            dot.node(den0[0], shape="record", label="{{{}|{}|{}}}".format(den0[0], den0[1], den0[2]))
            dot.node(den1[0], shape="record", label="{{{}|{}|{}}}".format(den1[0], den1[1], den1[2]))
        return dot

    def get_keyvalue(self, line, key):
        """return value of the key in line dict

        Parameters
        ----------
        line: dict
        key: key of the dict

        Returns
        -------
        value of the key
        """
        if key in line.keys():
            value = line[key]
        else:
            value = None
        return value

    def gen_connection_link_link(self, linklist, plinktype=None, plinkname=None, pnodetype=None):
        """generate connection among linklist

        Parameters
        ----------
        linklist: a list of link

        plinktype: string
            type of the parent link

        plinkname: string
            name of the parent link

        pnodetype: string
            name of the parent node

        Reeturns
        --------
        None
        """
        if linklist is None:
            return
        if plinkname is not None:
            pnodename = plinkname
            for linkline in linklist:
                name = self.get_keyvalue(linkline, "nodename")
                linktype = self.get_keyvalue(linkline, "linktype")
                link = self.get_keyvalue(linkline, "link")
                nodetype = self.get_keyvalue(linkline, "nodetype")
                self.den_edgelist.append([[pnodename, pnodetype, plinktype],
                                          [name, nodetype, linktype]])

        if plinkname is None:
            for linkline in linklist:
                name = self.get_keyvalue(linkline, "nodename")
                linktype = self.get_keyvalue(linkline, "linktype")
                link = self.get_keyvalue(linkline, "link")
                nodetype = self.get_keyvalue(linkline, "nodetype")
                self.gen_connection_link_link(link, linktype, name, nodetype)
        else:
            if plinktype == "part-of" or plinktype == "or" or plinktype is None:
                funcnamelist = []
                for linkline in linklist:
                    name = self.get_keyvalue(linkline, "nodename")
                    linktype = self.get_keyvalue(linkline, "linktype")
                    link = self.get_keyvalue(linkline, "link")
                    nodetype = self.get_keyvalue(linkline, "nodetype")

                    # funcp->methodp edge
                    funcp = self.func_prefix(pnodetype) + plinkname
                    methodp = self.method_prefix(pnodetype) + plinkname

                    if plinkname not in self.excludenodelist:
                        self.edgelist.append(",".join([funcp, methodp]))
                        self.boxnodelist.append(methodp)

                    # methodp->func edge
                    func1 = self.func_prefix(nodetype) + name
                    self.edgelist.append(",".join([methodp, func1]))

                    funcnamelist.append(func1)

                    self.gen_connection_link_link(link, linktype, name, nodetype)

                applyp = self.applyfunction_prefix(pnodetype) + plinkname

                self.applynodelist.append(applyp)
                self.edgelist.append(",".join([methodp, applyp]))
                funcnamelist.append(applyp)
                self.invisedgelist.append(",".join(funcnamelist))
                self.sameranklist.append(",".join(funcnamelist))

            elif plinktype == "is-a" or plinktype == "xor":

                namelist = []
                for linkline in linklist:
                    name = self.get_keyvalue(linkline, "nodename")
                    linktype = self.get_keyvalue(linkline, "linktype")
                    link = self.get_keyvalue(linkline, "link")
                    nodetype = self.get_keyvalue(linkline, "nodetype")

                    # print(">",plinkname,plinktype,"->",name,nodetype,link,linktype)

                    # no_mf = False

                    namelist.append(name)

                    # funcp->method1 edge
                    # method1 -> func1 edge
                    funcp = self.func_prefix(pnodetype) + plinkname
                    methodp = self.method_prefix(pnodetype) + plinkname
                    func1 = self.func_prefix(nodetype) + name
                    method1 = self.method_prefix(nodetype) + name

                    self.isanodelist.append(funcp)
                    if not method1.endswith(" way"):
                        method1 = method1 + " way"
                    # print("edge:funcp->method1",[funcp,method1])
                    self.edgelist.append(",".join([funcp, method1]))
                    if linktype != "part-of":
                        # print("edge:method1->func1",[method1,func1])
                        self.edgelist.append(",".join([method1, func1]))

                    self.boxnodelist.append(method1)
                    self.isaboxnodelist.append(method1)
                    self.excludenodelist.append(name)

                    self.gen_connection_link_link(link, linktype, name, nodetype)

            elif plinktype == "FunctionFirst":
                namelist = []
                for linkline1, linkline2 in zip(linklist[:-1], linklist[1:]):

                    name1 = self.get_keyvalue(linkline1, "nodename")
                    linktype1 = self.get_keyvalue(linkline1, "linktype")
                    link1 = self.get_keyvalue(linkline1, "link")
                    nodetype1 = self.get_keyvalue(linkline1, "nodetype")

                    name2 = self.get_keyvalue(linkline2, "nodename")
                    linktype2 = self.get_keyvalue(linkline2, "linktype")
                    link2 = self.get_keyvalue(linkline2, "link")
                    nodetype2 = self.get_keyvalue(linkline2, "nodetype")

                    funcp = self.func_prefix(pnodetype) + plinkname
                    methodp = self.method_prefix(pnodetype) + plinkname
                    func1 = self.func_prefix(nodetype1) + name1
                    method1 = self.method_prefix(nodetype1) + name1
                    func2 = self.func_prefix(nodetype2) + name2
                    method2 = self.method_prefix(nodetype2) + name2
                    apply2 = self.applyfunction_prefix(nodetype2) + name2

                    # generate links
                    self.edgelist.append(",".join([func2, method2]))
                    self.boxnodelist.append(method2)
                    self.edgelist.append(",".join([method2, func1]))
                    self.edgelist.append(",".join([method2, apply2]))
                    self.invisedgelist.append(",".join([func1, apply2]))
                    self.sameranklist.append(",".join([func1, apply2]))

                    self.gen_connection_link_link(link1, linktype1, name1, nodetype1)
                    self.gen_connection_link_link(link2, linktype2, name2, nodetype2)

            else:
                print("not supported, linktype=", plinktype)
                raise

    def linktree(self):
        """generate link tree

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        data = self.data
        linktype = self.get_keyvalue(data, "linktype")
        if "link" in list(data.keys()):
            self.gen_connection_link_link([data], linktype)


class FDTree(object):
    """Functional Decomposition Tree class
    """

    def __init__(self, basename="caus", dottree=None, dotoption=None):
        """initilization

        Parameters
        ----------
        basename: string
            name of the Digraph

        dottree: Digraph object or None
            create Digraph if it is None

        dotoption: dict
            options to pass Digraph

        Returns
        -------
        None
        """
        self.dotoption = None
        if dotoption is None:
            self.dotoption = {"nodelabel_length": 15}
        else:
            self.dotoption = dotoption

        self.dottree = None
        if dottree is None:
            print("FDTree:init generate dotreee")
            self.dottree = Digraph(basename)
            # self.dottree = Graph(basename)
            self.dottree.graph_attr["rankdir"] = "TB"
            if "splines" in self.dotoption:
                self.dottree.graph_attr["splines"] = self.dotoption["splines"]
            else:
                self.dottree.graph_attr["splines"] = "line"
            print("cencentrate{}".format(str(self.dotoption["concentrate"])))
            self.dottree.graph_attr["concentrate"] = str(self.dotoption["concentrate"])
            self.dottree.edge_attr["len"] = "2.2"
        else:
            self.dottree = dottree

    def apply(self, dataall, basename=None, make_png=True):
        """make Digraph diagram

        Parameters
        ----------
        dataall: diagram data
            it is read from json filename

        basename: string
            name of Digraph

        make_png: boolean
            create png if True

        Returns
        -------
        Digraph object
        """
        if basename is None:
            basename = "caus"

        dotoption = self.dotoption
        dottree = self.dottree

        gen_wf = dotoption["gen_wf"]
        gen_taxo = dotoption["gen_taxo"]
        print("gen_wf,gen_taxo", gen_wf, gen_taxo)

        for key in dataall:
            data = dataall[key]

            if key == "workflow":
                wf = workflowWay(dotoption=dotoption)
                wf.load(data={"workflow": data})
                wf.linktree()
                dottree = wf.create_tree(dottree)

                if gen_wf:
                    print("Digraph, basename", basename)
                    dotwf = Digraph(basename)
                    dotwf.graph_attr["rankdir"] = "BT"
                    dotwf.graph_attr["splines"] = "line"
                    dotwf = wf.create_workflow(dotwf)
                    dotwf.format = "png"
                    dotwf.render(view=False)
                    print("png is made.")

            elif key == "linkset":
                taxo = taxologyWay(dotoption=dotoption)

                for ataxo in data["block"]:
                    taxo.load(data=ataxo)
                    taxo.linktree()
                    dottree = taxo.create_tree(dottree)

                if gen_taxo:
                    print("Digraph, basename", basename)
                    dottaxo = Digraph(basename)
                    dottaxo.graph_attr["rankdir"] = "TB"
                    dottaxo = taxo.create_dendrogram(dottaxo)
                    dottaxo.format = "png"
                    dottaxo.render(view=False)
                    print("png is made.")

        if make_png:
            dottree.format = "png"
            dottree.render(view=False)
            print("png is made.")

        return dottree

    def apply_files(self, namelist):
        """execute .apply() from files in namelist

        Parameters
        ----------
        namelist: list
            a list of files to read

        Returns
        -------
        None
        """
        # dotoption = self.dotoption
        dottree = self.dottree

        for filename in namelist:

            basename, ext = os.path.splitext(filename)

            with open(filename) as f:
                dataall = yaml.safe_load(f)

            self.apply(dataall, make_png=False)

        if True:
            dottree.format = "png"
            dottree.render(view=False)
            print("png is made.")
