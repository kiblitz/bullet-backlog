import sqlite3

def on_tasks(path, *argv):
  db_path = path + 'tasks.db'
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  for arg in argv:
    arg(c)
  conn.commit()
  c.close()
  conn.close() 

def create_tasks_db(path):
  on_tasks(path + 'tasks.db', create_task_tables)

def create_task_tables(cursor):
  create_task_table(cursor)
  create_tag_table(cursor)
  create_child_table(cursor)
  create_parent_table(cursor)

def delete_task_tables(cursor):
  delete_task_table(cursor)
  delete_tag_table(cursor)
  delete_child_table(cursor)
  delete_parent_table(cursor)

def create_task_table(cursor):
  cursor.execute('''CREATE TABLE tasks
                (task_id INTEGER, title TEXT, body TEXT)''')

def create_tag_table(cursor):
  cursor.execute('''CREATE TABLE tags
                (task_id INTEGER, tag TEXT)''')

def create_child_table(cursor):
  cursor.execute('''CREATE TABLE children
                (task_id INTEGER, child_id INTEGER)''')

def create_parent_table(cursor):
  cursor.execute('''CREATE TABLE parent
                (task_id INTEGER, parent_id INTEGER)''')

def delete_task_table(cursor):
  cursor.execute('''DELETE FROM tasks''')

def delete_tag_table(cursor):
  cursor.execute('''DELETE FROM tags''')

def delete_child_table(cursor):
  cursor.execute('''DELETE FROM children''')

def delete_parent_table(cursor):
  cursor.execute('''DELETE FROM parent''')
