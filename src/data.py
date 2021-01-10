import db_handler
import dir_handler
import errors

def get():
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return
  return db_handler.get_all(path)
