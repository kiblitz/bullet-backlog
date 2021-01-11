
def bullet_exists():
  return __err_format('Bullet already exists')

def no_item():
  return __err_format('No item type specified')

def unknown_item(new):
  return __err_format('Unknown item type <%s>' % new)

def no_tags():
  return __err_format('No tags specified')

def no_task():
  return __err_format('No task id specified')

def no_subtask():
  return __err_format('No subtask id specified')

def task_not_found(task_id):
  return __err_format('Unrecognized task id <%s>' % task_id)

def subtask_not_found(subtask_id):
  return __err_format('Unrecognized subtask id <%s>' % subtask_id)

def self_relative():
  return __err_format('Cannot relate task with itself')

def no_bullet():
  return __err_format('No bullet found')

def invalid_status(code):
  return __err_format('Invalid status <%s>' % code)

def invalid_level(code):
  return __err_format('Invalid level <%s>' % code)

def invalid_date():
  return __err_format('Invalid date (\'MM/DD/YYYY\' or \'none\')')

def no_attribute():
  return __err_format('No attribute specified')

def no_attribute_value():
  return __err_format('No attribute value specified')

def no_relatives():
  return __err_format('No relative specified')

def relation_exists(parent_id, child_id):
  return __err_format('Relation <%s> -> <%s> already exists' % (parent_id, child_id))

def creates_loop(parent_id, child_id):
  return __err_format('Relation <%s> -> <%s> creates ancestral loop' % (parent_id, child_id))

def unknown_attribute(attribute):
  return __err_format('Unknown attribute <%s>' % attribute)

def unknown_visual_mode(mode):
  return __err_format('Unknown visual mode %s' % mode)


def unknown(comm):
  return __err_format('Unrecognized command <%s>' % comm)

def assertion_failure():
  return __err_format('Assertion failure: report bug')

def __err_format(error):
  return 'Error: %s' % error
