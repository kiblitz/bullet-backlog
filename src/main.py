#!/usr/bin/python

import sys

import descriptions
import dir_handler
import errors
import init
import new

def main():
  args = sys.argv
  num = len(args)
  if num == 1:
    print(descriptions.help()) 
    return
  if args[1] == 'init':
    # TODO init animation
    if not dir_handler.has_bullet():
      init.init()
    else:
      print(errors.bullet_exists()) 
    init.init()
  elif args[1] == 'new':
    new.new()
  else:
    print(descriptions.unknown())

if __name__ == "__main__":
  main()
