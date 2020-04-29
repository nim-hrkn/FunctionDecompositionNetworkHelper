#!/usr/bin/env python 
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


def load(filename):
    data = None
    with open(filename) as f:
        data = yaml.safe_load(f)

    return data

def apply_link(data,filename):
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

def wf_add_tag_filename(blocklist,filename):

    print("blocklist")
    print(blocklist)
    print("=----------")
    wfblockall = []
    for i,wf in enumerate(blocklist):

        print("wf before")
        print(yaml.dump(wf))
        print("-------")


        if wf["blockname"] is None or len(wf["blockname"])==0:
            wf["blockname"] = "{}#{}".format(filename,i)
        wf.update({"filename":filename})
        print("wf after")
        print(yaml.dump(wf))
        print("-------")

        wfblockall.append( copy.deepcopy(wf) )

    print("wfblockall")
    print(yaml.dump(wfblockall))
    print("-------------")
    return wfblockall

def lk_add_tag_filename(blocklist,filename):
    linkblockall = []
    for link in blocklist:
        print("link")
        print(yaml.dump(link))
        #link.update({"filename":filename})
        #linkblockall.extend(apply_link(link,filename) )
        linkblockall.extend(link )
    return linkblockall

def load_all_yml(filenames):
   dataall = {}

   wfblockall =  []
   lkblockall = []

   for filename in filenames:
      data = load(filename)
      print("load_all_yml,filename=",filename)
      print(yaml.dump(data))
      print("--------------")
      for key in data:
          if key=="workflow":
              data = wf_add_tag_filename(data[key]["block"],filename)
              wfblockall.extend(data)
          elif key=="linkset":
              #data = lk_add_tag_filename(data[key]["block"],filename)
              ablock = data[key]["block"]
              print(yaml.dump(ablock))
              lkblockall.extend(ablock)

   print("wkblockall")
   print(yaml.dump(wfblockall))
   print("-------")
   print("lkblockall")
   print(yaml.dump(lkblockall))
   print(lkblockall)
   print("-------")

   output = OrderedDict([("workflow",{ "block": wfblockall}), ("linkset",{"block": lkblockall} )] )
   return output

if __name__ == "__main__":

   wkall = load_all_yml(sys.argv[1:])
   filenameout = "a.yml"
   with open(filenameout,"w") as f: 
       yaml.dump(wkall,f)
       print("output to",filenameout)

