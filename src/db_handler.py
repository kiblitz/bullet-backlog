import sqlite3

idx = 0

def create_tasks_db(path):
  __on_tasks(path, __create_task_tables)

def delete_tasks_db(path):
  __on_tasks(path, __delete_task_tables)

def reset_tasks_db(path):
  __on_tasks(path, __delete_task_tables, __create_task_tables)

def new_task(path, title, body, tags, parents, children):
  __on_tasks_with_args(path, 
    (__create_task, title, body), 
    (__create_task_tags, tags), 
    (__create_task_parents, parents), 
    (__create_task_children, children))

def task_exists(task_id):
  return len(__on_tasks_with_args(path, (__select, 'tasks', '*', 'task_id=' + str(task_id)))) != 0 

def __insert(cursor, table, columns, args):
  sql = "INSERT INTO " + table + totuple(columns) + " VALUES" + qmark_args(len(args))
  cursor.execute(sql, args)
  return cursor.lastrowid

def __update(cursor, table, what, conditions):
  sql = "UPDATE " + table + " SET " + what + " " + conditions
  cursor.execute(sql)
  return cursor.lastrowid

def __select(cursor, table, what, conditions):
  sql = "SELECT " + what + " FROM " + table + " " + conditions
  cursor = conn.cursor()
  return cursor.execute(sql).fetchall()

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
  for arg in argv:
    arg(c)
  conn.commit()
  c.close()
  conn.close() 

def __on_tasks_with_args(path, *argv):
  db_path = path + 'tasks.db'
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  for arg in argv:
    arg[0](c, arg[1:])
  conn.commit()
  c.close()
  conn.close() 

def __create_task(cursor, title, body):
  global idx
  idx = __insert(cursor, 'tasks', ('title', 'body'), (title, body)) 

def __create_task_tags(cursor, tags):
  for tag in tags:
    __insert(cursor, 'tags', ('task_id', 'tag'), (idx, tag)) 

def __create_task_parents(cursor, parents):
  for parent in parents:
    __insert(cursor, 'parents', ('task_id', 'parent_id'), (idx, parent)) 
    __insert(cursor, 'children', ('task_id', 'child_id'), (parent, idx)) 

def __create_task_children(cursor, children):
  for child in children:
    __insert(cursor, 'children', ('task_id', 'child_id'), (idx, child)) 
    __insert(cursor, 'parents', ('task_id', 'parent_id'), (child, idx)) 

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
                (task_id INTEGER PRIMARY KEY, title TEXT, body TEXT)''')

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
