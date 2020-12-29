import db_handler
import dir_handler
import errors

def tag(task_id, tags):
  if not tags:
    print(errors.no_tags())
    return
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return
  if not db_handler.task_exists(path, task_id):
    print(errors.task_not_found(task_id))
    return

  db_handler.tag_task(path, task_id, tags)
