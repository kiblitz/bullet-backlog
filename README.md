# bullet-backlog
## About
Command line interface task management tool powered by python and sqlite3

## Install
### From Github
- Clone this repo and go into the repo directory
```
$ git clone https://github.com/thisistrivial/bullet-backlog.git
$ cd bullet-backlog
```
- Download `pyinstaller` and package the repo code
```
pip install pyinstaller
pyinstaller -D src/main.py -n bullet
```
- Make bullet a terminal command by creating a symbolic link
```
ln -s dist/bullet/bullet /usr/bin/
```
## How to Use
### Help Message
```
usage: bullet [--help|help]                                                     (0)
       bullet new task [<title>] [<body>...]                                    (1)
       bullet new subtask <task_id> [<title>] [<body>...]                       (2)
       bullet delete (task|subtask) <bullet_id> [--confirm|confirm]             (3)
       bullet (<command>) <task_id> [<args>...]                                 (4)
       bullet set (task|subtask) <bullet_id> (<attribute>) <val>                (5)
       bullet show [--all|--relevant|--unfinished|--<filter> [<args>]...]...    (6)

(0) view this help message

(1) create a new task
    ○ if no arguments provided, title and body will be prompted
    ○ if only one argument <arg> is provided, title=<arg> and body will be prompted
    ex: bullet new task sample_title this is a sample body

(2) create a new subtask under task <task_id>
    ○ if no arguments provided, title and body will be prompted
    ○ if only one argument <arg> is provided, title=<arg> and body will be prompted
    ex: bullet new subtask 1

(3) delete an existing bullet (task|subtask)
    ○ if confirmation not provided, confirmation will be prompted
    ex: bullet delete subtask 4 --confirm

(4) add relations/tags to an existing task <task_id>
    ○ commands: tag, untag, parent, unparent, child, unchild
    ○ tag: an attribute of a task
    ○ parent: if task <a> is a parent of task <b>, then <b> relies on <a>
    ○ child: if task <a> is a child of task <b>, then <a> relies on <b>
    ex: bullet tag 2 python sql cli

(5) edit attribute values for an existing bullet <bullet_id>
    ○ attributes: title, body, status, level, startdate, enddate, location
    ○ level: an integer representing the importance of a bullet
       ○ 0: none
       ○ 1: low
       ○ 2: normal
       ○ 3: high
       ○ 4: critical
    ○ status: an integer representing the progress status of a bullet
       ○ 0: none
       ○ 1: incomplete
       ○ 2: todo
       ○ 3: in progress
       ○ 4: complete
    ex: bullet set task 2 status 3

(6) visualize bullets in the terminal with stacking filters
    ○ filters: --all, --relevant, --unfinished, --tags_any, --tags_all, location
    ○ --all: show all tasks
    ○ --relevant: filter out tasks whose parents are not complete
    ○ --unfinished: filter out finished tasks
    ○ --tags_any: only show tasks with any of the specified tags
    ○ --tags_all: only show tasks with at least all of the specified tags
    ○ --location: only show tasks with any of the specified locations
```
