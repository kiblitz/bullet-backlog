import announce
import db_handler
import dir_handler
import errors

def task(task_id):
  res = __delete(db_handler.delete_task, 
                 task_id, 
                 db_handler.task_exists, 
                 errors.task_not_found)
  if res:
    print(announce.delete_task(task_id))

def subtask(subtask_id):
  res = __delete(db_handler.delete_subtask, 
                 subtask_id, 
                 db_handler.subtask_exists, 
                 errors.subtask_not_found)
  if res:
    print(announce.delete_subtask(subtask_id))

def __delete(action, task_id, exists, exists_error):
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return

  if not task_id.isdigit() or not exists(path, task_id):
    print(exists_error(task_id))
    return

  action(path, task_id)
  return True
