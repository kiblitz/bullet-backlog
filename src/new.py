import db_handler
import dir_handler
import errors

def new(title_given, title, body_given, body):
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return

  if not title_given:
    title = input('title: ')
  if not body_given:
    body = input('body: ')

  db_handler.new_task(path, title, body)
