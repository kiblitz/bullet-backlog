import sqlite3
import errors

def create_tasks_db(path):
  __on_tasks(path, __create_task_tables)

def delete_tasks_db(path):
  __on_tasks(path, __delete_task_tables)

def reset_tasks_db(path):
  __on_tasks(path, __delete_task_tables, __create_task_tables)

def new_task(path, title, body):
  __on_tasks_with_args(path, (__create_task, title, body))

def new_subtask(path, task_id, title, body):
  __on_tasks_with_args(path, (__create_subtask, task_id, title, body))

def delete_task(path, task_id):
  __on_tasks_with_args(path, (__remove_task, task_id))

def delete_subtask(path, task_id):
  __on_tasks_with_args(path, (__remove_subtask, subtask_id))

def tag_task(path, task_id, tags):
  __on_tasks_with_args(path, (__create_task_tags, task_id, tags))

def untag_task(path, task_id, tags):
  __on_tasks_with_args(path, (__remove_task_tags, task_id, tags))

def parent_task(path, task_id, parents):
  __on_tasks_with_args(path, (__create_task_parents, task_id, parents))

def unparent_task(path, task_id, parents):
  __on_tasks_with_args(path, (__remove_task_parents, task_id, parents))

def child_task(path, task_id, children):
  __on_tasks_with_args(path, (__create_task_children, task_id, children))

def unchild_task(path, task_id, children):
  __on_tasks_with_args(path, (__remove_task_children, task_id, children))

def set_task_status(path, task_id, status):
  __on_tasks_with_args(path, (__update_task_status, task_id, status))

def set_task_level(path, task_id, level):
  __on_tasks_with_args(path, (__update_task_level, task_id, level))

def set_task_startdate(path, task_id, date):
  __on_tasks_with_args(path, (__update_task_startdate, task_id, date))

def set_task_enddate(path, task_id, date):
  __on_tasks_with_args(path, (__update_task_enddate, task_id, date))

def set_task_location(path, task_id, location):
  __on_tasks_with_args(path, (__update_task_location, task_id, location))

def set_subtask_status(path, subtask_id, status):
  __on_tasks_with_args(path, (__update_subtask_status, subtask_id, status))

def set_subtask_level(path, subtask_id, level):
  __on_tasks_with_args(path, (__update_subtask_level, subtask_id, level))

def set_subtask_startdate(path, subtask_id, date):
  __on_tasks_with_args(path, (__update_subtask_startdate, subtask_id, date))

def set_subtask_enddate(path, subtask_id, date):
  __on_tasks_with_args(path, (__update_subtask_enddate, subtask_id, date))

def set_subtask_location(path, subtask_id, location):
  __on_tasks_with_args(path, (__update_subtask_location, subtask_id, location))

def get_all(path):
  data = __on_tasks_with_args(path, 
                              (__select, 'tasks', '*', 'TRUE'),
                              (__select, 'subtasks', '*', 'TRUE'),
                              (__select, 'tags', '*', 'TRUE'),
                              (__select, 'parents', '*', 'TRUE'),
                              (__select, 'children', '*', 'TRUE'),
                              row_factory=sqlite3.Row)
  data_dict = {}
  tables = ('tasks', 'subtasks', 'tags', 'parents', 'children')
  for i in range(len(tables)):
    data_dict[tables[i]] = data[i]
  return data_dict

def task_exists(path, task_id):
  return len(__on_tasks_with_args(path, (__select, 'tasks', '*', 'task_id=' + str(task_id)))[0]) != 0

def subtask_exists(path, subtask_id):
  return len(__on_tasks_with_args(path, (__select, 'subtasks', '*', 'subtask_id=' + str(subtask_id)))[0]) != 0

def to_text(value):
  return '\'%s\'' % value

def __create_task(cursor, title, body):
  __insert(cursor, 'tasks', ('title', 'body'), (title, body))

def __create_subtask(cursor, task_id, title, body):
  __insert(cursor, 'subtasks', ('task_id', 'title', 'body'), (task_id, title, body))

def __create_task_tags(cursor, task_id, tags):
  for tag in tags:
    __insert(cursor, 'tags', ('task_id', 'tag'), (task_id, tag))

def __create_task_parents(cursor, task_id, parents):
  for parent in parents:
    if __will_create_loop(cursor, parent, task_id):
      print(errors.creates_loop(parent, task_id))
      break
    if __relation_exists(cursor, parent, task_id):
      print(errors.relation_exists(parent, task_id))
      break
    __insert(cursor, 'parents', ('task_id', 'parent_id'), (task_id, parent))
    __insert(cursor, 'children', ('task_id', 'child_id'), (parent, task_id))

def __create_task_children(cursor, task_id, children):
  for child in children:
    if __will_create_loop(cursor, task_id, child):
      print(errors.creates_loop(task_id, child))
      break
    if __relation_exists(cursor, task_id, child):
      print(errors.relation_exists(task_id, child))
      break
    __insert(cursor, 'children', ('task_id', 'child_id'), (task_id, child))
    __insert(cursor, 'parents', ('task_id', 'parent_id'), (child, task_id))

def __remove_task(cursor, task_id):
  __remove(cursor, 'tasks', 'task_id=%s' % task_id)
  __remove(cursor, 'tags', 'task_id=%s' % task_id)
  __remove(cursor, 'parents', 'task_id=%s OR parent_id=%s' % (task_id, task_id))
  __remove(cursor, 'children', 'task_id=%s OR child_id=%s' % (task_id, task_id))
  __remove(cursor, 'subtasks', 'task_id=%s' % task_id)

def __remove_subtask(cursor, subtask_id):
  __remove(cursor, 'subtasks', 'subtask_id=%s' % subtask_id)

def __remove_task_tags(cursor, task_id, tags):
  for tag in tags:
    __remove(cursor, 'tags', 'task_id=%s AND tag=\'%s\'' % (task_id, tag))

def __remove_task_parents(cursor, task_id, parents):
  for parent in parents:
    __remove(cursor, 'parents', 'task_id=%s AND parent_id=%s' % (task_id, parent))
    __remove(cursor, 'children', 'task_id=%s AND child_id=%s' % (parent, task_id))

def __remove_task_children(cursor, task_id, children):
  for child in children:
    __remove(cursor, 'children', 'task_id=%s AND child_id=%s' % (task_id, child))
    __remove(cursor, 'parents', 'task_id=%s AND parent_id=%s' % (child, task_id))

def __update_task_status(cursor, task_id, status):
  __update(cursor, 'tasks', 'status=%s' % status, 'task_id=%s' % task_id)

def __update_task_level(cursor, task_id, level):
  __update(cursor, 'tasks', 'level=%s' % level, 'task_id=%s' % task_id)

def __update_task_startdate(cursor, task_id, date):
  __update(cursor, 'tasks', 'startdate=%s' % date, 'task_id=%s' % task_id)

def __update_task_enddate(cursor, task_id, date):
  __update(cursor, 'tasks', 'enddate=%s' % date, 'task_id=%s' % task_id)

def __update_task_location(cursor, task_id, location):
  __update(cursor, 'tasks', 'location=%s' % location, 'task_id=%s' % task_id)

def __update_subtask_status(cursor, subtask_id, status):
  __update(cursor, 'subtasks', 'status=%s' % status, 'subtask_id=%s' % subtask_id)

def __update_subtask_level(cursor, subtask_id, level):
  __update(cursor, 'subtasks', 'level=%s' % level, 'subtask_id=%s' % subtask_id)

def __update_subtask_startdate(cursor, subtask_id, date):
  __update(cursor, 'subtasks', 'startdate=%s' % date, 'subtask_id=%s' % subtask_id)

def __update_subtask_enddate(cursor, subtask_id, date):
  __update(cursor, 'subtasks', 'enddate=%s' % date, 'subtask_id=%s' % subtask_id)

def __update_subtask_location(cursor, subtask_id, location):
  __update(cursor, 'subtasks', 'location=%s' % location, 'subtask_id=%s' % subtask_id)

def __relation_exists(cursor, first_id, second_id):
  return ((int(second_id),) in __select(cursor, 'children', 'child_id', 'task_id=%s' % first_id) 
       or (int(second_id),) in __select(cursor, 'children', 'task_id', 'child_id=%s' % first_id))

def __insert(cursor, table, columns, args):
  sql = "INSERT INTO " + table + __totuple(columns) + " VALUES" + __qmark_args(len(args))
  cursor.execute(sql, args)
  return cursor.lastrowid

def __update(cursor, table, what, conditions):
  sql = "UPDATE " + table + " SET " + what + " WHERE " + conditions
  cursor.execute(sql)
  return cursor.lastrowid

def __remove(cursor, table, conditions):
  sql = "DELETE FROM " + table + " WHERE " + conditions
  cursor.execute(sql)
  return cursor.lastrowid

def __select(cursor, table, what, conditions):
  sql = "SELECT " + what + " FROM " + table + " WHERE " + conditions
  cursor.execute(sql)
  return cursor.fetchall()

def __on_tasks(path, *argv, row_factory=None):
  db_path = path + 'tasks.db'
  conn = sqlite3.connect(db_path)
  conn.row_factory = row_factory
  c = conn.cursor()
  res = []
  for arg in argv:
    res.append(arg(c))
  conn.commit()
  c.close()
  conn.close()
  return res

def __on_tasks_with_args(path, *argv, row_factory=None):
  db_path = path + 'tasks.db'
  conn = sqlite3.connect(db_path)
  conn.row_factory = row_factory
  c = conn.cursor()
  res = []
  for arg in argv:
    res.append(arg[0](c, *arg[1:]))
  conn.commit()
  c.close()
  conn.close()
  return res

def __create_task_tables(cursor):
  __create_task_table(cursor)
  __create_subtask_table(cursor)
  __create_tag_table(cursor)
  __create_child_table(cursor)
  __create_parent_table(cursor)

def __delete_task_tables(cursor):
  __delete_task_table(cursor)
  __delete_subtask_table(cursor)
  __delete_tag_table(cursor)
  __delete_child_table(cursor)
  __delete_parent_table(cursor)

def __create_task_table(cursor):
  cursor.execute('''CREATE TABLE tasks
                (task_id INTEGER PRIMARY KEY, 
                 title TEXT, 
                 body TEXT, 
                 startdate TEXT DEFAULT 'none',
                 enddate TEXT DEFAULT 'none',
                 location TEXT DEFAULT 'none',
                 status INT DEFAULT 0,
                 level INT DEFAULT 0)''')

def __create_subtask_table(cursor):
  cursor.execute('''CREATE TABLE subtasks
                (subtask_id INTEGER PRIMARY KEY, 
                 task_id INT,
                 title TEXT, 
                 body TEXT, 
                 startdate TEXT DEFAULT 'none',
                 enddate TEXT DEFAULT 'none',
                 location TEXT DEFAULT 'none',
                 status INT DEFAULT 0,
                 level INT DEFAULT 0)''')

def __create_tag_table(cursor):
  cursor.execute('''CREATE TABLE tags
                (task_id INTEGER, tag TEXT)''')

def __create_child_table(cursor):
  cursor.execute('''CREATE TABLE children
                (task_id INTEGER, child_id INTEGER)''')

def __create_parent_table(cursor):
  cursor.execute('''CREATE TABLE parents
                (task_id INTEGER, parent_id INTEGER)''')

def __delete_task_table(cursor):
  cursor.execute('''DELETE FROM tasks''')

def __delete_subtask_table(cursor):
  cursor.execute('''DELETE FROM subtasks''')

def __delete_tag_table(cursor):
  cursor.execute('''DELETE FROM tags''')

def __delete_child_table(cursor):
  cursor.execute('''DELETE FROM children''')

def __delete_parent_table(cursor):
  cursor.execute('''DELETE FROM parents''')

def __will_create_loop(cursor, parent, child):
  nodes = [parent]
  seen = {parent}
  while nodes and int(child) not in nodes:
    first = nodes[0]
    comm = 'SELECT parent_id FROM parents where task_id=%s' % first
    lst = list(map(lambda x: x[0], cursor.execute(comm).fetchall()))
    new_lst = [elem for elem in lst if elem not in seen]
    nodes = nodes[1:] 
    nodes.extend(new_lst)
    seen.update(new_lst)
  return int(child) in nodes

def __qmark_args(num):
  s = '('
  for i in range(num - 1):
    s += '?,'
  return s + '?)'

def __totuple(args):
  s = '('
  for arg in args:
    s += arg + ','
  return s[:len(s)-1] + ')'

