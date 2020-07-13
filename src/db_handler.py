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
  on_tasks(path + 'tasks.db', create_task_table)

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
