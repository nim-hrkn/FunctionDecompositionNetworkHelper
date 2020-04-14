#!/usr/bin/env python
import sys
import yaml

if len(sys.argv)>2:
    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
else:
    print("usage: thisfile inputfile outputfile")
    sys.exit(1)

print("input,output=",inputfilename,outputfilename)

with open(inputfilename) as f:
    lines = f.read()
    lines = lines.split("\n")

workflowlist = []

for line in lines:
    line = line.rstrip()
    if len(line)==0:
        continue
    title,content = line.split(":")
    print (title,content)
    x = content.split("[")
    zlist = []
    for y in x:
        if len(y)==0:
            continue
        z = y.split("]")
        print(z)
        zlist.append(z)

    group = []
    i = len(zlist)
    while i>0:
        i = i-1
        z = zlist[i]
        if z[0].startswith("2)"):
            group = []
            group.append({"group": [{"methodname":z[0], "funcname":z[1],"functype":"parts"}]})
            i = i-1
            z = zlist[i]
            if len(z[0])==0:
               group1 = { "funcname":z[1],"functype":"parts"}
            else:
               group1 = {"methodname":z[0], "funcname":z[1],"functype":"parts"}
            i = i-1
            z = zlist[i]
            if len(z[0])==0:
               group2 = { "funcname":z[1],"functype":"parts"}
            else:
               group2 = {"methodname":z[0], "funcname":z[1],"functype":"parts"}
            group.append({"group": [group1,group2]})
        elif len(z[0])==0:
            # no method
            group.append({"group": [{"funcname":z[1], "functype":"parts"}]})
        else:
            group.append({"group": [{"methodname":z[0], "funcname":z[1],"functype":"parts"}]})

    group = list(reversed(group))

    workflow =  {"groupname":title, "workflow": group } 
    print(workflow)
    workflowlist.append( workflow )

workflowall = {"workflow":workflowlist}
with open(outputfilename, "w" ) as f:
    s = yaml.dump(workflowall)
    f.write(s)

