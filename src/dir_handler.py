import os

def mk_bullet():
  os.mkdir('.bullet')
  return __append_bullet_folder(os.getcwd())

def has_bullet():
  return os.path.isdir('.bullet')

def find_bullet():
  path = os.getcwd()
  while True:
    with_bullet = __append_bullet_folder(path)
    if os.path.isdir(with_bullet):
      return with_bullet
    if path == '/':
      return False
    path = os.path.dirname(path)

def __append_bullet_folder(path):
  return path + '/.bullet/'
