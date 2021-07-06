# Function Decomposition Network Helper
needs graphviz inside.

version 0.3.0

# install & uninstall

## to install
```
$ python setup.py install
```
It will automatically install graphviz, too.

## to uninstall
```
$ python setup.py install --record=installedfiles.txt
```
and delete files in installedfiles.txt


# samples

## DescriptorTargetVariable
```
cd sample/DescriptorTargetVariable
$ make
```

## MaterialsExploration
```
$ cd sample/MaterialsExploration
$ make
```

## BookReading
```
$ cdb BookReading
$ make
```

## TIPS
They make cau.gv to pass graphviz-dot in the make command.
For example,
```
neato cau.gv -Tpng > neato.Tpng
```
can create a graphviz-neato diagram.

# format

The description consists of workflow parts and is-a relation parts.

## workflow
```
workflow:
  block:
  - blockname: CD CT
    list:
    - group:
      - outputname: crystal desriptor satisfying all invariance
    - group:
      - wayname: association with crystal descriptor and crystal target variable way
        outputname: association with descriptor and crystal target variable satisfying all invariance

  - blockname: AD AT CT
    list:
    - group:
      - outputname: all atomic descriptors satisfying coordinate invariance
    - group:
      - wayname: Atomic descriptor to crystal target way
        outputname: atomic target variable satisfying all invariance
    - group:
      - wayname: Atomic target to crystal atarget association way
        outputname: association with descriptor and crystal target variable satisfying all invariance
```

- The function decomposition chain is defined as
[(wayname) - outputname] - ... - [wayname - outputname]. The first wayname can be omittied.
- The minimum size chain is a pair of wayname - outputname], [(wayname) - outputname] - [wayname - outputname].
- outputname adds "Obtain" to create the node, "Obtain \<outputname\>".
- If outputtype: "direct" is added, the outputname is directly the node name, so you can write a verb.

## is-a relation
```
linkset:
  block:
  - link:
    - nodename: association with descriptor and crystal target variable
      linktype: is-a
      link:
      - nodename: association with descriptor and crystal target variable satisfying all invariance
        linktype: is-a
      - nodename: association with descriptor and crystal target variable not satisfying all invariance
        linktype: is-a

  - link:
    - nodename: crystal desriptor satisfying all invariance
      linktype: is-a
      link:
      - nodename: crystal desriptor satisfying all invariance from atomic descriptors
        linktype: is-a
        link:
        - nodename: crystal desriptor satisfying all invariance from all atomic descripotrs by min.
        - nodename: crystal desriptor satisfying all invariance from all atomic descripotrs by max.
```

- nodename adds "Obtain" to create the node, "Obtain \<nodename\>".
