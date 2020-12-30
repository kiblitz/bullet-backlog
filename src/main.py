#!/usr/bin/python

import sys

import descriptions
import dir_handler
import errors
import init
import new
import relate
import tag

def __main():
  args = sys.argv
  num = len(args)
  if num == 1 or args[1] in __get_flags('help'):
    print(descriptions.help())
    return
  if args[1] == 'init':
    init.init()
  elif args[1] == 'new':
    rest = args[2:]
    title_given = False
    body_given = False
    title = ''
    body = ''
    while rest:
      if rest[0] == '--title':
        if len(rest) > 1:
          title_given = True 
          title = rest[1]
        else:
          print(errors.no_title())
          return
      if rest[0] == '--body':
        if len(rest) > 1:
          body_given = True 
          body = rest[1]
        else:
          print(errors.no_body())
          return
      rest = rest[2:]
    new.new(title_given, title, body_given, body)
  elif args[1] in ('tag', 'untag', 'parent', 'unparent', 'child', 'unchild'):
    if num < 3:
      print(errors.no_task())
      return
    task = args[2]
    stuff = args[3:]
    if args[1] == 'tag':
      tag.tag(task, stuff)
    elif args[1] == 'untag':
      tag.untag(task, stuff)
    elif args[1] == 'parent':
      relate.parent(task, stuff)
    elif args[1] == 'unparent':
      relate.unparent(task, stuff)
    elif args[1] == 'child':
      relate.child(task, stuff)
    else:
      relate.unchild(task, stuff)
  else:
    print(descriptions.unknown(args[1]))

def __get_flags(keyword):
  pre = ('', '--')
  return (p + keyword for p in pre)

if __name__ == "__main__":
  __main()

