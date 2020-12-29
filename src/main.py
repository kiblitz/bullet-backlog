#!/usr/bin/python

import sys

import descriptions
import dir_handler
import errors
import init
import new
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
  elif args[1] == 'tag':
    if num < 3:
      print(errors.no_task())
      return
    task = args[2]
    tags = args[3:]
    tag.tag(task, tags)
  else:
    print(descriptions.unknown())

def __get_flags(keyword):
  pre = ('', '--')
  return (p + keyword for p in pre)

if __name__ == "__main__":
  __main()

