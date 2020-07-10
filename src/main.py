#!/usr/bin/python

import sys

import descriptions

def main():
  args = sys.argv
  num = len(args)
  if num == 1:
    print(descriptions.help()) 
    return
  if args[1] == '':
    pass
  elif args[1] == '':
    pass
  else:
    print(descriptions.unknown())
    
if __name__ == "__main__":
  main()
