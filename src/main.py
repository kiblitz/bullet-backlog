#!/usr/bin/python

import sys

import descriptions
import dir_handler
import errors
import init
import new
import relate
import tag
import task_attributes

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
    if rest:
      title_given = True 
      title = rest[0]
      rest = rest[1:]
    if rest:
      body_given = True
      body = ' '.join(rest).replace('\n', '').strip()
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
  elif args[1] == 'set':
    if num < 3:
      print(errors.no_attribute())
    if args[2] in ('status', 'level', 'startdate', 'enddate', 'location'):
      if num < 4:
        print(errors.no_task())
        return
      task = args[3]
      if num < 5:
        print(errors.no_attribute_value())
        return
      if args[2] == 'status':
        task_attributes.set_status(task, args[4])
      elif args[2] == 'level':
        task_attributes.set_level(task, args[4])
      elif args[2] == 'startdate':
        task_attributes.set_startdate(task, args[4])
      elif args[2] == 'enddate':
        task_attributes.set_enddate(task, args[4])
      else:
        task_attributes.set_location(task, args[4])
    else:
      print(errors.unknown_attribute(args[2]))
  else:
    print(descriptions.unknown(args[1]))

def __get_flags(keyword):
  pre = ('', '--')
  return (p + keyword for p in pre)

if __name__ == "__main__":
  __main()

