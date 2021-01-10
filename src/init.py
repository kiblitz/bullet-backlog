import announce
import db_handler
import dir_handler
import errors

def init():
  if not dir_handler.has_bullet():
    path = dir_handler.mk_bullet()
    db_handler.create_tasks_db(path)
    print(announce.init())
  else:
    print(errors.bullet_exists())
