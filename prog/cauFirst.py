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
import sys
import yaml
from graphviz import Digraph

from FuncDecompHelper import FDTree


if __name__ == "__main__":

    import argparse

    def parse_cmd_option():
        parser = argparse.ArgumentParser()
        parser.add_argument("filenames", nargs="*")
        parser.add_argument("--gen_wf", action="store_true")
        parser.add_argument("--gen_taxo", action="store_true")
        parser.add_argument("--no_connect_invis", dest="connect_invis", action="store_true")
        parser.add_argument("--no_concentrate", dest="concentrate", action="store_false")
        parser.add_argument("--samerank", default=None)
        parser.add_argument("--doit", default="all")

        cmdopt = parser.parse_args()

        return cmdopt

    def doit_each(namelist, dotoption):

        dottree = Digraph("caus")
        dottree.graph_attr["rankdir"] = "TB"
        dottree.graph_attr["concentrate"] = str(dotoption["concentrate"])+";"

        for filename in namelist:

            basename, ext = os.path.splitext(filename)
            print("doit_each, basename", basename)

            with open(filename) as f:
                dataall = yaml.safe_load(f)

            fdtree = FDTree(basename, dottree, dotoption=dotoption)
            dottree = fdtree.apply(dataall, basename=basename, make_png=False)

        dottree.format = "png"
        dottree.render(view=False)
        print("done")

    # start

    cmdopt = parse_cmd_option()
    print(cmdopt)
    namelist = cmdopt.filenames

    if len(namelist) == 0:
        sys.exit(1)

    doit = cmdopt.doit

    if doit == "each":
        doit_each(namelist, cmdopt.__dict__)

    elif doit == "all":

        fdtree = FDTree(dotoption=cmdopt.__dict__)
        dottree = fdtree.apply_files(namelist)
