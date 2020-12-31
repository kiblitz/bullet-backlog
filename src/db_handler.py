import sqlite3

def create_tasks_db(path):
  __on_tasks(path, __create_task_tables)

def delete_tasks_db(path):
  __on_tasks(path, __delete_task_tables)

def reset_tasks_db(path):
  __on_tasks(path, __delete_task_tables, __create_task_tables)

def new_task(path, title, body):
  __on_tasks_with_args(path, (__create_task, title, body))

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
  __on_tasks_with_args(path, (__set_task_status, task_id, status))

def set_task_level(path, task_id, level):
  __on_tasks_with_args(path, (__set_task_level, task_id, level))

def __create_task(cursor, title, body):
  __insert(cursor, 'tasks', ('title', 'body'), (title, body))

def __create_task_tags(cursor, task_id, tags):
  for tag in tags:
    __insert(cursor, 'tags', ('task_id', 'tag'), (task_id, tag))

def __create_task_parents(cursor, task_id, parents):
  for parent in parents:
    __insert(cursor, 'parents', ('task_id', 'parent_id'), (task_id, parent))
    __insert(cursor, 'children', ('task_id', 'child_id'), (parent, task_id))

def __create_task_children(cursor, task_id, children):
  for child in children:
    __insert(cursor, 'children', ('task_id', 'child_id'), (task_id, child))
    __insert(cursor, 'parents', ('task_id', 'parent_id'), (child, task_id))

def __remove_task(cursor, task_id):
  __remove(cursor, 'tasks', 'task_id=%s' % task_id)
  __remove(cursor, 'tags', 'task_id=%s' % task_id)
  __remove(cursor, 'parents', 'task_id=%s OR parent_id=%s' % (task_id, task_id))
  __remove(cursor, 'children', 'task_id=%s OR child_id=%s' % (task_id, task_id))

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

def __set_task_status(cursor, task_id, status):
  __update(cursor, 'tasks', 'status=%s' % status, 'task_id=%s' % task_id)

def __set_task_level(cursor, task_id, level):
  __update(cursor, 'tasks', 'level=%s' % level, 'task_id=%s' % task_id)

def task_exists(path, task_id):
  return len(__on_tasks_with_args(path, (__select, 'tasks', '*', 'task_id=' + str(task_id)))[0]) != 0

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

def __on_tasks(path, *argv):
  db_path = path + 'tasks.db'
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  res = []
  for arg in argv:
    res.append(arg(c))
  conn.commit()
  c.close()
  conn.close()
  return res

def __on_tasks_with_args(path, *argv):
  db_path = path + 'tasks.db'
  conn = sqlite3.connect(db_path)
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
  __create_tag_table(cursor)
  __create_child_table(cursor)
  __create_parent_table(cursor)

def __delete_task_tables(cursor):
  __delete_task_table(cursor)
  __delete_tag_table(cursor)
  __delete_child_table(cursor)
  __delete_parent_table(cursor)

def __create_task_table(cursor):
  cursor.execute('''CREATE TABLE tasks
                (task_id INTEGER PRIMARY KEY, 
                 title TEXT, 
                 body TEXT, 
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

def __delete_tag_table(cursor):
  cursor.execute('''DELETE FROM tags''')

def __delete_child_table(cursor):
  cursor.execute('''DELETE FROM children''')

def __delete_parent_table(cursor):
  cursor.execute('''DELETE FROM parents''')
