import db_handler
import errors

def new():
  path = find_bullet()
  if not path:
    print(errors.no_bullet()) 
    return

  title = input('title: ')
  body = input('body: ')

  tags = []
  tag = input('tags: ')
  while tag != '':
    tags.append(tag)
    tag = input('tags: ') 

  parents = []
  parent = input('parents: ')
  while parent != '':
    # TODO check if id exists
    if True:
      parents.append(parent)
    else:
      print('task id <' + parent + '> not found') 
    parent = input('parents: ')  

  children = []
  child = input('children: ')
  while child != '':
    # TODO check if id exists
    if True:
      children.append(child)
    else:
      print('task id <' + child + '> not found') 
    child = input('children: ')  

  db_handler.new_task(path, title, body, tags, parents, children)
