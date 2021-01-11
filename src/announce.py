
def init():
  return 'Created bullet in this folder'

def new_task(title, body):
  return 'Created new task -> %s: %s' % (title, body)

def new_subtask(task_id, title, body):
  return 'Created new subtask under task (%s) -> %s: %s' % (task_id, title, body)

def title_set(task_id, title):
  return __attr_set('task', task_id, 'title', title)

def subtask_title_set(subtask_id, title):
  return __attr_set('subtask', subtask_id, 'title', title)

def body_set(task_id, body):
  return __attr_set('task', task_id, 'body', body)

def subtask_body_set(subtask_id, body):
  return __attr_set('subtask', subtask_id, 'body', body)

def status_set(task_id, status):
  return __attr_set('task', task_id, 'status', status)

def subtask_status_set(subtask_id, status):
  return __attr_set('subtask', subtask_id, 'status', status)

def level_set(task_id, level):
  return __attr_set('task', task_id, 'level', level)

def subtask_level_set(subtask_id, level):
  return __attr_set('subtask', subtask_id, 'level', level)

def startdate_set(task_id, date):
  return __attr_set('task', task_id, 'startdate', date)

def subtask_startdate_set(subtask_id, date):
  return __attr_set('subtask', subtask_id, 'startdate', date)

def enddate_set(task_id, date):
  return __attr_set('task', task_id, 'enddate', date)

def endtask_startdate_set(subtask_id, date):
  return __attr_set('subtask', subtask_id, 'enddate', date)

def location_set(task_id, location):
  return __attr_set('task', task_id, 'location', location)

def subtask_location_set(subtask_id, location):
  return __attr_set('subtask', subtask_id, 'location', location)

def tagged(task_id, tags):
  return __relation_set('Added', 'tags', task_id, tags)

def untagged(task_id, tags):
  return __relation_set('Removed', 'tags', task_id, tags)

def parented(task_id, parents):
  return __relation_set('Added', 'parents', task_id, parents)

def unparented(task_id, parents):
  return __relation_set('Removed', 'parents', task_id, parents)

def childed(task_id, children):
  return __relation_set('Added', 'children', task_id, children)

def unchilded(task_id, children):
  return __relation_set('Removed', 'children', task_id, children)

def __relation_set(action, relation_type, task_id, relation_ids):
  return '%s task (%s) %s: (%s)' % (action, task_id, relation_type, ','.join(relation_ids))

def __attr_set(entry_type, entry_id, value_type, value):
  return 'Set %s for %s (%s) to %s' % (value_type, entry_type, entry_id, value)
