import datetime

import announce
import db_handler
import dir_handler
import errors

def set_status(task_id, status):
  if not get_status(status):
    return
  res = __manage_attributes(db_handler.set_task_status, task_id, status)
  if res:
    print(announce.status_set(task_id, get_status(status)))

def set_level(task_id, level):
  if not get_level(level):
    return
  res = __manage_attributes(db_handler.set_task_level, task_id, level)
  if res:
    print(announce.level_set(task_id, get_level(level)))

def set_startdate(task_id, date):
  res = __set_date(db_handler.set_task_startdate, task_id, date)
  if res:
    print(announce.startdate_set(task_id, date))

def set_enddate(task_id, date):
  res = __set_date(db_handler.set_task_enddate, task_id, date)
  if res:
    print(announce.enddate_set(task_id, date))

def set_location(task_id, location):
  res = __manage_attributes(db_handler.set_task_location, 
                            task_id, 
                            db_handler.to_text(location))
  if res:
    print(announce.location_set(task_id, location))

def set_subtask_status(subtask_id, status):
  if not get_status(status):
    return
  res = __manage_attributes(db_handler.set_subtask_status, 
                            subtask_id, 
                            status,
                            db_handler.subtask_exists,
                            errors.subtask_not_found)
  if res:
    print(announce.subtask_status_set(subtask_id, get_status(status)))

def set_subtask_level(subtask_id, level):
  if not get_level(level):
    return
  res = __manage_attributes(db_handler.set_subtask_level, 
                            subtask_id, 
                            level,
                            db_handler.subtask_exists,
                            errors.subtask_not_found)
  if res:
    print(announce.subtask_level_set(subtask_id, get_level(level)))

def set_subtask_startdate(subtask_id, date):
  res = __set_date(db_handler.set_subtask_startdate, 
                   subtask_id, 
                   date,
                   db_handler.subtask_exists,
                   errors.subtask_not_found)
  if res:
    print(announce.subtask_startdate_set(subtask_id, date))

def set_subtask_enddate(subtask_id, date):
  res = __set_date(db_handler.set_subtask_enddate, 
                   subtask_id, 
                   date,
                   db_handler.subtask_exists,
                   errors.subtask_not_found)
  if res:
    print(announce.subtask_enddate_set(subtask_id, date))

def set_subtask_location(subtask_id, location):
  res = __manage_attributes(db_handler.set_subtask_location, 
                            subtask_id, 
                            db_handler.to_text(location),
                            db_handler.subtask_exists,
                            errors.subtask_not_found)
  if res:
    print(announce.subtask_location_set(subtask_id, location))

def __set_date(action, 
               task_id, 
               date, 
               task_exist_checker=db_handler.task_exists, 
               task_not_found_error=errors.task_not_found):
  date = date.lower()
  if date != 'none':
    try:
      spldate = date.split('/')
      if len(spldate) != 3:
        raise Exception()
      datetime.datetime(month=int(spldate[0]), 
                        day=int(spldate[1]), 
                        year=int(spldate[2]))
    except:
      print(errors.invalid_date())
      return
  return __manage_attributes(action, 
                             task_id, 
                             db_handler.to_text(date), 
                             task_exist_checker, 
                             task_not_found_error)

def __manage_attributes(action, 
                        task_id, 
                        value, 
                        task_exist_checker=db_handler.task_exists, 
                        task_not_found_error=errors.task_not_found):
  path = dir_handler.find_bullet()
  if not path:
    print(errors.no_bullet())
    return
  if not task_id.isdigit() or not task_exist_checker(path, task_id):
    print(task_not_found_error(task_id))
    return
  action(path, task_id, value)
  return True

def get_status(code):
  code = str(code)
  if code == '0':
    return 'None'
  if code == '1':
    return 'Incomplete'
  if code == '2':
    return 'Todo'
  if code == '3':
    return 'In Progress'
  if code == '4':
    return 'Complete'
  print(errors.invalid_status(code))

def get_level(code):
  code = str(code)
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
