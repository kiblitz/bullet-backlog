import consts
import data
import db_handler
import task_attributes

def show(argv):
  __show(argv)

def only_relevant(tasks_dict, tag_rows_dict, tables):
  parents = tables['parents']
  for i in range(len(parents)):
    task_id = parents[i]['task_id']
    parent_id = parents[i]['parent_id']
    parent_level = tasks_dict[parent_id]['status']
    if parent_level != consts.STATUS_COMPLETE:
      tasks_dict.pop(task_id, None)
  return tasks_dict

def only_unfinished(tasks_dict, tag_rows_dict, tables):
  filtered_dict = {k:v for (k,v) in tasks_dict.items() 
                   if v['status'] != consts.STATUS_COMPLETE}
  return filtered_dict

def tags_any_filter(tasks_dict, tag_rows_dict, tables, *tags):
  filtered_dict = {k:v for (k,v) in tasks_dict.items()
                   if (k in tag_rows_dict and 
                       any(tag in tag_rows_dict[k] for tag in tags))}
  return filtered_dict

def tags_all_filter(tasks_dict, tag_rows_dict, tables, *tags):
  filtered_dict = {k:v for (k,v) in tasks_dict.items()
                   if (k in tag_rows_dict and 
                       all(tag in tag_rows_dict[k] for tag in tags))}
  return filtered_dict

def location_filter(tasks_dict, tag_rows_dict, tables, *locations):
  filtered_dict = {k:v for (k,v) in tasks_dict.items()
                   if (any(area.lower() == v['location'].lower() 
                   for area in locations))}
  return filtered_dict

def __show(argv):
  tables = data.get()
  tasks_dict = __get_tasks_dict(tables)
  subtasks_dict = __get_subtasks_dict(tables)
  tag_rows_dict = __get_tag_rows_dict(tables)
  for arg in argv:
    func = arg[0]
    args = arg[1:]
    tasks_dict = func(tasks_dict, tag_rows_dict, tables, *args)
  print('')
  for task_id in tasks_dict:
    task_row = tasks_dict[task_id]
    tag_rows = tag_rows_dict.get(task_id)
    subtask_rows = subtasks_dict.get(task_id)
    print(__with_subtasks(__task_all(task_row, tag_rows), 
          subtask_rows, 
          __task_main))

def __get_tasks_dict(tables):
  tasks = tables['tasks']
  tasks_dict = {}
  for i in range(len(tasks)):
    tasks_dict[tasks[i]['task_id']] = tasks[i]
  return tasks_dict

def __get_tag_rows_dict(tables):
  tag_rows_dict = {}
  tags = tables['tags']
  for tag in tags:
    task_id = tag['task_id']
    if not task_id in tag_rows_dict:
      tag_rows_dict[task_id] = [] 
    tag_rows_dict[task_id].append(tag['tag'])
  return tag_rows_dict

def __get_subtasks_dict(tables):
  subtasks = tables['subtasks']
  subtasks_dict = {}
  for subtask_row in subtasks:
    task_id = subtask_row['task_id']
    if task_id not in subtasks_dict:
      subtasks_dict[task_id] = []
    subtasks_dict[task_id].append(subtask_row)
  return subtasks_dict

def __task_minimal(task_row, key='task_id'):
  return '○ (%s) %s' % (task_row[key], task_row['title'])

def __task_basic(task_row, key='task_id'):
  return '%s: %s' % (__task_minimal(task_row, key), task_row['body'])

def __task_attributes(task_row):
  status = task_row['status']
  level = task_row['level']
  startdate = task_row['startdate']
  enddate = task_row['enddate']
  location = task_row['location']
  ret = ''
  if status != consts.STATUS_NONE:
    ret += ' {%s}' % task_attributes.get_status(status)
  if level != consts.LEVEL_NONE:
    ret += ' {%s}' % task_attributes.get_level(level)

  if startdate == 'none':
    startdate = ''
  if enddate == 'none':
    enddate = ''
  if startdate or enddate:
    ret += ' (%s ─ %s)' % (startdate, enddate)

  if location != 'none':
    ret += ' (%s)' % location
  if not ret:
    return None
  return '|' + ret

def __task_tags(tag_rows):
  if not tag_rows:
    return None
  ret = ''
  for tag in tag_rows:
    ret += '[%s] ' % tag
  return '| ' + ret[:-1]

def __task_main(task_row, key='task_id'):
  basic = __task_basic(task_row, key)
  attr = __task_attributes(task_row)
  ret = '%s\n' % basic
  if attr:
    ret += '%s\n' % attr
  return ret

def __task_all(task_row, tag_rows, key='task_id'):
  tags = __task_tags(tag_rows)
  ret = __task_main(task_row, key)
  if tags:
    ret += '%s\n' % tags
  return ret

def __with_subtasks(task_text, subtask_rows, subtask_representation):
  ret = task_text
  if subtask_rows:
    for subtask_row in subtask_rows:
      subtask_rep = subtask_representation(subtask_row, 'subtask_id')
      subtask_split = subtask_rep.split('\n')
      subtask_lst = ([subtask_split[0]] + ['|  ' + 
                     subtask_elem for subtask_elem in subtask_split[1:-1]])
      subtask_str = '\n'.join(subtask_lst)
      ret += '|  |\n|  %s\n' % subtask_str
  ret += '|'
  return ret
