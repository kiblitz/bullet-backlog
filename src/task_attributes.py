import datetime

import db_handler
import dir_handler
import errors

def set_status(task_id, status):
  if not get_status(status):
    return
  __manage_attributes(db_handler.set_task_status, task_id, status)

def set_level(task_id, level):
  if not get_level(level):
    return
  __manage_attributes(db_handler.set_task_level, task_id, level)

def set_startdate(task_id, date):
  __set_date(db_handler.set_task_startdate, task_id, date)

def set_enddate(task_id, date):
  __set_date(db_handler.set_task_enddate, task_id, date)

def __set_date(action, task_id, date):
  date = date.lower()
  if date != 'none':
    try:
      spldate = date.split('-')
      if len(spldate) != 3:
        raise Exception()
      datetime.datetime(month=int(spldate[0]), 
                        day=int(spldate[1]), 
                        year=int(spldate[2]))
    except:
      print(errors.invalid_date())
      return
  __manage_attributes(action, task_id, db_handler.to_text(date))

def __manage_attributes(action, task_id, value):
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return
  if not task_id.isdigit() or not db_handler.task_exists(path, task_id):
    print(errors.task_not_found(task_id))
    return
  action(path, task_id, value)

def get_status(code):
  if code == '0':
    return 'None'
  if code == '1':
    return 'Incomplete'
  if code == '2':
    return 'Todo'
  if code == '3':
    return 'In Progress'
  if code == '4':
    return 'Completed'
  print(errors.invalid_status(code))

def get_level(code):
  if code == '0':
    return 'None'
  if code == '1':
    return 'Low'
  if code == '2':
    return 'Normal'
  if code == '3':
    return 'High'
  if code == '4':
    return 'Critical'
  print(errors.invalid_level(code))
