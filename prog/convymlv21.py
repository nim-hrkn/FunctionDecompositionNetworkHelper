#!/usr/bin/env python 
import yaml
import sys
import os

from collections import OrderedDict
from ruamel.yaml import YAML, add_constructor, resolver

if True:
    def represent_odict(dumper, instance):
        return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

    yaml.add_representer(OrderedDict, represent_odict)

    def construct_odict(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)

def load_yml(filename):
    data = None
    with open(filename) as f:
        data = yaml.safe_load(f)

    return data

class workflow_format_V21:

    def __init__(self):
        pass 

    def change_group(self,group):
        groups = []
        for g in group:
            dic = OrderedDict()

            try:
                funcname = g["funcname"]
            except:
                funcname = None
            try:
                functype = g["functype"]
            except:
                functype = None
            try:
                methodname = g["methodname"]
            except:
                methodname = None
            try:
                methodtype = g["methodtype"]
            except:
                methodtype = None

            if methodname is not None and methodtype is not None:
                dic1 = OrderedDict([( 'methodname',methodname), ('methodtype',methodtype)] )
                dic.update(dic1)
            if methodname is not None and methodtype is None:
                dic1 = OrderedDict([( 'methodname',methodname) ] )
                dic.update(dic1)

            if funcname is not None and functype is not None:
                dic1 = OrderedDict([( 'funcname',funcname), ('functype',functype)]  )
                dic.update(dic1)
            if funcname is not None and functype is None:
                dic1 = OrderedDict([('funcname',funcname)]  )
                dic.update(dic1)
            groups.append(dic)
        return groups


    def change_glist(self,glist):
    #    print("-glist",glist)
        glistnew = []
        for group in glist:
            groupsnew = self.change_group(group["group"])
            glistnew.append({"group":groupsnew})
    #    print("glistnew>",glistnew)
        #print(yaml.dump(glistnew))
        return glistnew

    def convert(self,data):
       if "link" in data.keys():
           print("link found, do nothing.")
           return data
       wflist = []
       for x in data:
           for y in data[x]:
               wfname =  y["groupname"]
               if wfname is not None and len(wfname)==0:
                   wfname = None
               glist = self.change_glist(y["workflow"])

               workflowpart = {"blockname":wfname,"order":"workflow", "list":glist }
               wflist.append(workflowpart)

       wf = {"workflow":{"format":"v2.1", "block":wflist}}
       return wf


class workflow_format_V22:

    def __init__(self):
        pass 

    def change_group(self,group):
        groups = []
        for g in group:
            g = dict(g)
            dic = OrderedDict()

            try:
                funcname = g["funcname"]
            except:
                funcname = None
            try:
                functype = g["functype"]
            except:
                functype = None
            try:
                methodname = g["methodname"]
            except:
                methodname = None
            try:
                methodtype = g["methodtype"]
            except:
                methodtype = None

            if methodname is not None and methodtype is not None:
                dic1 = OrderedDict([( 'methodname',methodname), ('methodtype',methodtype)] )
                dic.update(dic1)
            if methodname is not None and methodtype is None:
                dic1 = OrderedDict([( 'methodname',methodname) ] )
                dic.update(dic1)

            if funcname is not None and functype is not None:
                dic1 = OrderedDict([( 'outputname',funcname), ('outputtype',functype)]  )
                dic.update(dic1)
            if funcname is not None and functype is None:
                dic1 = OrderedDict([('outputname',funcname)]  )
                dic.update(dic1)
            groups.append(dic)
        return groups


    def change_glist(self,glist):
    #    print("-glist",glist)
        glistnew = []
        for group in glist:
            print("group",group)
            groupsnew = self.change_group(group["group"])
            glistnew.append({"group":groupsnew})
    #    print("glistnew>",glistnew)
        #print(yaml.dump(glistnew))
        return glistnew

    def convert(self,data):
       if "link" in data.keys():
           print("link found, do nothing.")
           return data
       wflist = []
       block = data["workflow"]
       for x in block["block"]:
           wfname =  x["blockname"]
           if wfname is not None and len(wfname)==0:
               wfname = None

           glist = self.change_glist(x["list"])

           workflowpart = {"blockname":wfname,"order":"workflow", "list":glist }
           wflist.append(workflowpart)

       wf = {"workflow":{"format":"v2.2", "block":wflist}}
       return wf


def dump_yaml(wf,filename_out):

   yaml = YAML()
   yaml.default_flow_style = False

   if os.path.exists(filename_out):
       raise FileExistsError("filename {} exists. abort".format(filename_out))
   else:
       with open(filename_out,"w") as f:
           print(yaml.dump(wf,f))
           print("yaml dumped to",filename_out)


if __name__ == "__main__":

   if len(sys.argv)==3:
       filename_in = sys.argv[1]
       filename_out = sys.argv[2]
   else:
       raise SyntaxError("usage: prog filename_input filename_output")

   data = load_yml(filename_in)
   wf = workflow_format_V22()
   wfnew = wf.convert(data)
   print(wfnew)
   dump_yaml(wfnew,filename_out)


