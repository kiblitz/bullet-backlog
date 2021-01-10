import announce
import db_handler
import dir_handler
import errors

def task(title_given, title, body_given, body):
  res = __new(db_handler.new_task, 
              None,
              title_given, 
              title, 
              body_given, 
              body)
  if res:
    print(announce.new_task(res[0], res[1]))

def subtask(title_given, task_id, title, body_given, body):
  res = __new(db_handler.new_subtask, 
              task_id, 
              title_given, 
              title, 
              body_given, 
              body)
  if res:
    print(announce.new_subtask(res[0], res[1]))

def __new(action, task_id, title_given, title, body_given, body):
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return

  if task_id and (not task_id.isdigit() or not db_handler.task_exists(path, task_id)):
    print(errors.task_not_found(task_id))
    return

  if not title_given:
    title = input('title: ')
  if not body_given:
    body = input('body: ')

  if task_id: 
    action(path, task_id, title, body)
  else:
    action(path, title, body)
  return (title, body)
