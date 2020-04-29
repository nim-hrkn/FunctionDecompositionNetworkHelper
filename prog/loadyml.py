#!/usr/bin/env python 
import yaml
import sys

def load(filename):
    data = None
    with open(filename) as f:
        data = yaml.safe_load(f)

    return data

if __name__ == "__main__":
   data = load(sys.argv[1])
   print(yaml.dump(data))
