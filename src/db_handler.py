import sqlite3

def create_tasks_db(path):
  __on_tasks(path + 'tasks.db', __create_task_tables)

def delete_tasks_db(path):
  __on_tasks(path + 'tasks.db', __delete_task_tables)

def reset_tasks_db(path):
  __on_tasks(path + 'tasks.db', __delete_task_tables, __create_task_tables)

def new_task(path, title, body, tags, parents, children):
  __on_tasks_with_args(path, __create_task, title, body, tags, parents, children)

def __insert(conn, table, columns, args, autocommit=True):
  sql = "INSERT INTO " + table + totuple(columns) + " VALUES" + qmark_args(len(args))
  cursor = conn.cursor()
  cursor.execute(sql, args)
  if autocommit:
    conn.commit()
  return cursor.lastrowid

def __update(conn, table, what, conditions, autocommit=True):
  sql = "UPDATE " + table + " SET " + what + " " + conditions
  cursor = conn.cursor()
  cursor.execute(sql)
  if autocommit:
    conn.commit()
  return cursor.lastrowid

def __select(conn, table, what, conditions):
  cursor = conn.cursor()
  res = cursor.execute("SELECT " + what + " FROM " + table + " " + conditions)
  return res.fetchall()

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

def __on_tasks_with_args(path, func, *argv):
  db_path = path + 'tasks.db'
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  func(c, *argv)
  conn.commit()
  c.close()
  conn.close() 

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
                (task_id INTEGER, title TEXT, body TEXT)''')

def __create_tag_table(cursor):
  cursor.execute('''CREATE TABLE tags
                (task_id INTEGER, tag TEXT)''')

def __create_child_table(cursor):
  cursor.execute('''CREATE TABLE children
                (task_id INTEGER, child_id INTEGER)''')

def __create_parent_table(cursor):
  cursor.execute('''CREATE TABLE parent
                (task_id INTEGER, parent_id INTEGER)''')

def __delete_task_table(cursor):
  cursor.execute('''DELETE FROM tasks''')

def __delete_tag_table(cursor):
  cursor.execute('''DELETE FROM tags''')

def __delete_child_table(cursor):
  cursor.execute('''DELETE FROM children''')

def __delete_parent_table(cursor):
  cursor.execute('''DELETE FROM parent''')
