import os

def find_bullet():
  path = os.getcwd()
  while True:
    if os.path.isdir(path + '/.bullet'):
      return path + '/.bullet'
    if path == '/':
      return False
    path = __get_parent(path)

def __get_parent(directory):
  return os.path.dirname(directory)
