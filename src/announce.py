
def init():
  return 'Created bullet in this folder'

def new_task(title, body):
  return __new_entry('task', title, body)

def new_subtask(title, body):
  return __new_entry('subtask', title, body)

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

def parented(task_id, parents):
  return __relation_set('Added', 'parents', task_id, parents)

def unparented(task_id, parents):
  return __relation_set('Removed', 'parents', task_id, parents)

def childed(task_id, children):
  return __relation_set('Added', 'children', task_id, children)

def unchilded(task_id, children):
  return __relation_set('Removed', 'children', task_id, children)

def __new_entry(entry_type, title, body):
  return 'Created new %s - %s: %s' % (entry_type, title, body)

def __relation_set(action, relation_type, task_id, relation_ids):
  return '%s task (%s) %s: (%s)' % (action, task_id, relation_type, ','.join(relation_ids))

def __attr_set(entry_type, entry_id, value_type, value):
  return 'Set %s for %s (%s) to %s' % (value_type, entry_type, entry_id, value)
