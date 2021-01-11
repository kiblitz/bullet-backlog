import announce
import db_handler
import dir_handler
import errors

def tag(task_id, tags):
  res = __manage_tags(db_handler.tag_task, task_id, tags)
  if res:
    print(announce.tagged(task_id, tags))

def untag(task_id, tags):
  res = __manage_tags(db_handler.untag_task, task_id, tags)
  if res:
    print(announce.untagged(task_id, tags))

def __manage_tags(action, task_id, tags):
  if not tags:
    print(errors.no_tags())
    return
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return
  if not task_id.isdigit() or not db_handler.task_exists(path, task_id):
    print(errors.task_not_found(task_id))
    return
  action(path, task_id, tags)
  return True
