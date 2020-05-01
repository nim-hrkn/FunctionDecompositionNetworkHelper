import copy
from collections import OrderedDict

class WFChain(object):
    def __init__(self,wklist=None):
        if wklist is None:
            self.wklist = []
        else:
            self.wklist = wklist
            
    def extend(self,wfchain):
        self.wklist.extend(wfchain.wklist)
            
    def to_WF(self):
        wklist = self.wklist
        blocklist = []
        for wk in wklist:
            node1,node2 = wk
            if "methodname"  not in node2:
                print(node1)
                print(node2)
                raise
            name = node1["outputname"]+"-"+node2["methodname"]+"-"+node2["outputname"]
            gglist = OrderedDict( ( ("blockname", name),\
                                   ("order","workflow"),\
                      ("list", [{"group":[node1]}, {"group":[node2]} ] ) ) )
            blocklist.append(gglist)

        blocks = OrderedDict( ( ("format", "v2.3"), \
            ("block", blocklist) ) )
        wf = OrderedDict( {"workflow":blocks} )

        return wf
    
    def search_link(self,outputname1,outputname2):
        wklist = self.wklist        
        self.linklist = []
        self.search_link_inside(outputname1,outputname2)
        return self.get_selectedWFChain()
        
    def get_outputnames(self,wklist):
        namelist = []
        for node1, node2 in wklist:
            namelist.append(node1["outputname"])
            namelist.append(node2["outputname"])
        return list(set(namelist))

    def search_link_inside(self,outputname1,outputname2,link=[]):
        #print("search_link",outputname1,outputname2)
        if len(outputname1)==0:
            return []
        #print("link",link)
        wklist = self.wklist
        subwklist = []
        wklistnext = []
        for node1, node2 in wklist:
            if node1["outputname"] == outputname1:
                wklistnext.append( node2["outputname"] )
                #subwklist.append( [node1,node2])
                if outputname2 is not None:
                    if node2["outputname"] == outputname2:
                        link.append([outputname1,outputname2])
                        print("found link",link)
                        self.linklist.append(link)
                        return 

        wklistnext = list(set(wklistnext))
        #print("wklistnext",wklistnext)
        for newoutputname1 in wklistnext:
            newlink = copy.deepcopy(link)
            newlink.append([outputname1,newoutputname1])
            self.search_link_inside(newoutputname1,outputname2,newlink)
            
    def get_selectedWFChain(self):
        selectedlist = []
        wklist = self.wklist
        for link in self.linklist:
            for output1,output2 in link:
                for wk in wklist:
                    node1,node2 = wk
                    if node1["outputname"] == output1 and \
                       node2["outputname"] == output2 :
                        selectedlist.append( [copy.deepcopy(node1),copy.deepcopy(node2)])
        return WFChain(selectedlist)
        #return selectedlist
    
class wfblockToWFChaim(WFChain):
    def __init__(self,wfblockall):

        self.wfblockall = wfblockall
        
        wklist = self.wfblockallTowklist(wfblockall)        
        wklist.extend( self.wfblockallTowklist_fromLast(wfblockall) )
    
        self.wklist = wklist
        
    def wfblockallTowklist(self,wfblockall):
        #wfblockall = self.wfblockall
        wklist = []
        for block in wfblockall:
            blockname = block["blockname"]
            for alist1,alist2 in zip(block["list"][0:-1],block["list"][1:]):
                #print(">",alist1,alist2)
                group1 = alist1["group"]
                group2 = alist2["group"]
                for node1 in group1:
                    for node2 in group2:
                        wklist.append([copy.deepcopy(node1),copy.deepcopy(node2)])
        return wklist
    
    def search_connection(self,node):
        wklist = []
        outputname = node["outputname"]
        outputtype = None
        if "outputtype" in node:
            outputtype = node["outputtype"]
        for block in self.wfblockall:
            blockname = block["blockname"]
            for alist1,alist2 in zip(block["list"][0:-1],block["list"][1:]):
                group1 = alist1["group"]
                group2 = alist2["group"]
                for node1 , node2 in zip(group1,group2):
                    wklist.append([node1,node2])
                    if node1["outputname"] == node["outputname"] and \
                       node1["outputtype"] == node["outputtype"]:
                            #print("found>", node1,"->",node2)
                            wklist.append( [node1,node2])
        return wklist    
    
    def wfblockallTowklist_fromLast(self,wfblockall):
        #wfblockall = self.wfblockall
        wklist = []
        for block in wfblockall:
            blockname = block["blockname"]
            alist1 = block["list"][-1]["group"]
            #print (alist1)
            for node in alist1:
                outputname = node["outputname"]
                outputtype = None
                if "outputtype" in node:
                    outputtype = node["outputtype"]
                #print(outputname,outputtype)
                wklist.extend(self.search_connection(node))
        return wklist
  
