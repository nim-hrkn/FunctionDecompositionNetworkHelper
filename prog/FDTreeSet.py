#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8


import yaml
import sys
import copy

from collections import OrderedDict

if True:
    def represent_odict(dumper, instance):
        return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

    yaml.add_representer(OrderedDict, represent_odict)

    def construct_odict(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)

class FDTreeSet(object):
    def __init__(self):
        self.wfblockall = []
        self.lkblockall = []

    def load(self,filename):
        data = None
        with open(filename) as f:
            data = yaml.safe_load(f)
        return data

    def apply_link(self,data,filename):
        key1 = "link"
        linkcontent = ["nodename","nodetype","linktype"]
        linklist =  []
        for link in data[key1]:
            alink = []
            for content in linkcontent:
                if content in link.keys():
                    alink.append( (content,link[content]) )
            alink.append( ("filename",filename) )
            if "link" in link.keys():
                newlink = apply_link(link,filename)
                alink.append( ("link", newlink ) )
            linklist.append(  OrderedDict(alink) )
        return linklist

    def wf_add_tag_filename(self,blocklist,filename=None):


        wfblockall = []
        for i,wf in enumerate(blocklist):

            if wf["blockname"] is None or len(wf["blockname"])==0:
                wf["blockname"] = "{}#{}".format(filename,i)
            wf.update({"filename":filename})
            wfblockall.append( copy.deepcopy(wf) )

        return wfblockall

    def lk_add_tag_filename(self,blocklist):
        linkblockall = []
        for link in blocklist:

            #link.update({"filename":filename})
            #linkblockall.extend(apply_link(link,filename) )
            linkblockall.extend(link )
        return linkblockall

    def load_files(self,filenames):
        dataall = {}

        wfblockall = self.wfblockall
        lkblockall = self.lkblockall

        for filename in filenames:
          data = self.load(filename)

          for key in data:
              if key=="workflow":
                  data = self.wf_add_tag_filename(data[key]["block"],filename)
                  wfblockall.extend(data)
              elif key=="linkset":
                  #data = lk_add_tag_filename(data[key]["block"],filename)
                  ablock = data[key]["block"]
                  lkblockall.extend(ablock)

        self.wfblockall = wfblockall
        self.lkblockall = lkblockall
        

        #output = OrderedDict([("workflow",{ "block": wfblockall}), ("linkset",{"block": lkblockall} )] )
        #return output
    
    def export_dic(self):
        wfblockall = self.wfblockall
        lkblockall = self.lkblockall
        output = OrderedDict([("workflow",{ "block": wfblockall}), ("linkset",{"block": lkblockall} )] )
        return output
    
    def print_wf(self):
        for x in self.wfblockall:
            print("workflow:",x["blockname"])
            
    def print_lk(self):
        for x in self.lkblockall:
            print("link:",x["link"][0]["nodename"])
            
    def print_names(self,name=None):
        if name is None:
            self.print_wf()
            self.print_lk()
        if name in ["wf"]:
            self.print_wf()
        if name in ["lk"]:
            self.print_lk()

            

       

if __name__ == "__main__":



    import glob
    filenames = glob.glob("sample/*.yml")

    # CrystalTarget
    filenames = glob.glob("sample/CrystalTargetToDescriptor_*.yml")

    # TargetValuePrediction
    filenames = glob.glob("sample/TheoreticalTargetValuePrediction_*.yml")

    # AtomicProperty
    filenames = glob.glob("sample/AtomicProperty_Caus*.yml")

    # MaterialsList
    filenames = glob.glob("sample/MaterialsList_*.yml")

    #AtomicCoordinate2Descriptor
    filenames = glob.glob("sample/AtomicCoordinate2Descriptor_*.yml")

    #Importance
    filenames= glob.glob("sample/Importance_*.yml")

    #Group
    filenames= glob.glob("sample/Group_*.yml")

    #UnderstandingFiles
    Understanding_misc = [
    "sample/Understand_Taxo.yml",
    "sample/SparseModeling.yml",
    "sample/LinearModel_Taxo.yml",
    "sample/EXSparseModel.yml"]
    Understanding = Understanding_misc
    Understanding.extend(glob.glob("sample/Importance_*.yml"))
    Understanding.extend(glob.glob("sample/Group_*.yml"))

    filenames = Understanding


    fdtree = FDTreeSet()
    fdtree.load_files(filenames)





    fdtree.print_wf()





    fdtree.print_lk()





    dic = fdtree.export_dic()





    filename = "a.yml"
    with open(filename,"w") as f:
        yaml.dump(dic,f)













