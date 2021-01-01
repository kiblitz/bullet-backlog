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
    if num < 3:
      print(errors.no_item())
      return
    if args[2] in ('task', 'subtask'):
      rest = args[3:]
      if args[2] == 'subtask':
        if not rest:
          print(errors.no_task())
          return
        task_id = rest[0]
        rest = rest[1:]
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
      if args[2] == 'task':
        new.task(title_given, title, body_given, body)
      else:
        new.subtask(title_given, task_id, title, body_given, body)
    else:
      print(errors.unknown_item(args[2]))

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
      return
    set_commands = ('status', 'level', 'startdate', 'enddate', 'location')
    task_set_actions = (task_attributes.set_status, 
                           task_attributes.set_level,
                           task_attributes.set_startdate,
                           task_attributes.set_enddate,
                           task_attributes.set_location)
    subtask_set_actions = (task_attributes.set_subtask_status, 
                           task_attributes.set_subtask_level,
                           task_attributes.set_subtask_startdate,
                           task_attributes.set_subtask_enddate,
                           task_attributes.set_subtask_location)
    if args[2] == 'subtask':
      if num < 4:
        print(errors.no_attribute())
        return
      __handle_set_attribute(args[1:], 
                             set_commands, 
                             subtask_set_actions, 
                             errors.no_subtask, 
                             num - 1)
    else:
      __handle_set_attribute(args, 
                             set_commands, 
                             task_set_actions, 
                             errors.no_task, 
                             num)

  else:
    print(descriptions.unknown(args[1]))

def __handle_set_attribute(args, set_commands, set_actions, no_row_error, num):
  if args[2] in set_commands:
    if num < 4:
      print(no_row_error())
      return
    task = args[3]
    if num < 5:
      print(errors.no_attribute_value())
      return
    for i in range(len(set_commands)):
      if args[2] == set_commands[i]:
        set_actions[i](task, args[4])
        return
    print(errors.assertion_failure())
  else:
    print(errors.unknown_attribute(args[2]))

def __get_flags(keyword):
  pre = ('', '--')
  return (p + keyword for p in pre)

if __name__ == "__main__":
  __main()

