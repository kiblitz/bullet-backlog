import db_handler
import dir_handler
import errors

def parent(task_id, parents):
  __manage_relations(db_handler.parent_task, task_id, parents)

def unparent(task_id, parents):
  __manage_relations(db_handler.unparent_task, task_id, parents)

def child(task_id, children):
  __manage_relations(db_handler.child_task, task_id, children)

def unchild(task_id, children):
  __manage_relations(db_handler.unchild_task, task_id, children)

def __manage_relations(action, task_id, relatives):
  if not relatives:
    print(errors.no_relatives())
    return
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return
  if not task_id.isdigit() or not db_handler.task_exists(path, task_id):
    print(errors.task_not_found(task_id))
    return
  valid = True
  for relative in relatives:
    if not relative.isdigit() or not db_handler.task_exists(path, relative):
      print(errors.relative_not_found(relative))
      valid = False
  if not valid:
    return
  action(path, task_id, relatives)
