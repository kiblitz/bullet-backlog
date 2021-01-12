#!/usr/bin/python

import sys

import delete
import descriptions
import dir_handler
import errors
import init
import new
import relate
import tag
import task_attributes
import visual

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

  elif args[1] == 'delete':
    if num < 3:
      print(errors.no_item())
      return
    if args[2] in ('task', 'subtask'):
      if num < 4:
        if args[2] == 'task':
          print(errors.no_task())
        else:
          print(errors.no_subtask()) 
        return
      task_id = args[3] 
      rest = args[4:]
      confirmed = any(x in __get_flags('confirm') for x in rest)
      if args[2] == 'task':
        delete.task(task_id, confirmed)
      else:
        delete.subtask(task_id, confirmed)
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
      print(errors.no_item())
      return
    if args[2] in ('task', 'subtask'):
      rest = args[3:]
      rest_num = len(rest)
      if rest_num < 1:
        if args[2] == 'task':
          print(errors.no_task())
        else:
          print(errors.no_subtask()) 
        return
      __handle_set_attribute(args[2],
                             rest, 
                             rest_num)
    else:
      print(errors.unknown_item(args[2]))

  elif args[1] == 'show':
    rest = args[2:]
    filters = [(visual.only_relevant, )]
    stack = []
    for arg in rest:
      if arg == __get_flag('all'):
        filters = []
        stack = []
      elif arg == __get_flag('relevant'):
        __handle_visual_stack(filters, stack, arg)
        filters.append((visual.only_relevant, ))
      elif arg == __get_flag('unfinished'):
        __handle_visual_stack(filters, stack, arg)
        filters.append((visual.only_unfinished, ))
      elif arg in (__get_flag('tags_any'), 
                   __get_flag('tags_all'), 
                   __get_flag('location')):
        __handle_visual_stack(filters, stack, arg)
      else:
        if not stack:
          print(errors.unknown_visual_mode(arg))
          return
        stack.append(arg)
    __handle_visual_stack(filters, stack, '')
    visual.show(filters)
  else:
    print(errors.unknown(args[1]))

def __handle_visual_stack(filters, stack, arg):
  if stack:
    filters.append(stack.copy())
    stack.clear()
  comm = None
  if arg == __get_flag('tags_any'):
    comm = visual.tags_any_filter
  elif arg == __get_flag('tags_all'):
    comm = visual.tags_all_filter
  elif arg == __get_flag('location'):
    comm = visual.location_filter
  if comm:
    stack.append(comm)

def __handle_set_attribute(mode, args, num):
  set_commands = ('title', 
                  'body', 
                  'status', 
                  'level', 
                  'startdate', 
                  'enddate', 
                  'location')
  task_set_actions = (task_attributes.set_title,
                      task_attributes.set_body,
                      task_attributes.set_status, 
                      task_attributes.set_level,
                      task_attributes.set_startdate,
                      task_attributes.set_enddate,
                      task_attributes.set_location)
  subtask_set_actions = (task_attributes.set_subtask_title,
                         task_attributes.set_subtask_body,
                         task_attributes.set_subtask_status, 
                         task_attributes.set_subtask_level,
                         task_attributes.set_subtask_startdate,
                         task_attributes.set_subtask_enddate,
                         task_attributes.set_subtask_location)
  if mode == 'task':
    set_actions = task_set_actions
  else:
    set_actions = subtask_set_actions
  task = args[0]
  if num < 2:
    print(errors.no_attribute())
    return
  if args[1] in set_commands:
    if num < 3:
      print(errors.no_attribute_value())
      return
    for i in range(len(set_commands)):
      if args[1] == set_commands[i]:
        set_actions[i](task, ' '.join(args[2:]).strip())
        return
    print(errors.assertion_failure())
  else:
    print(errors.unknown_attribute(args[1]))

def __get_flag(keyword):
  return '--%s' % keyword

def __get_flags(keyword):
  pre = ('', '--')
  return (p + keyword for p in pre)

if __name__ == "__main__":
  __main()

