
def bullet_exists():
  return __err_format('Bullet already exists')

def no_tags():
  return __err_format('No tags specified')

def no_task():
  return __err_format('No task id specified')

def task_not_found(task_id):
  return __err_format('Unrecognized task id <%s>' % task_id)

def self_relative():
  return __err_format('Cannot relate task with itself')

def no_bullet():
  return __err_format('No bullet found')

def invalid_status(code):
  return __err_format('Invalid status <%s>' % code)

def invalid_level(code):
  return __err_format('Invalid level <%s>' % code)

def no_attribute():
  return __err_format('No attribute specified')

def __err_format(error):
  return 'Error: %s' % error
