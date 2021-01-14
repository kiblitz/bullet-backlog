# bullet-backlog
## About
Command line interface chain-based task management tool powered by python and sqlite3

## Install
### From Github
- Clone this repo and go into the repo directory
```
$ git clone https://github.com/thisistrivial/bullet-backlog.git
$ cd bullet-backlog
```
- Download `pyinstaller` and package the repo code
```
$ pip install pyinstaller
$ pyinstaller -D src/main.py -n bullet
```
- Make `bullet` a terminal command by creating a symbolic link
```
$ ln -s dist/bullet/bullet /usr/bin/
```
## How to Use
### Workflow
- Initialize a bullet-backlog in a project folder to manage its tasks
- Create new tasks
- Edit the task attributes and add tags to those tasks
- Establish an ancestral chain (if task `a` is a parent of task `b`, finish task `a` before starting task `b`)
- Create subtasks for tasks
- Edit the subtask attributes
- View visual backlog
### Level and Status codes
- **Level**: an integer representing the importance of a bullet
  - 0: none
  - 1: low
  - 2: normal
  - 3: high
  - 4: critical
- **Status**: an integer representing the progress status of a bullet
  - 0: none
  - 1: incomplete
  - 2: todo
  - 3: in progress
  - 4: complete
### Visual Filters
Sequentially filter out tasks when viewing the visual backlog
- **--all**: remove all filters
- **--relevant** (default): filter out tasks whose parents are not complete
- **--unfinished**: filter out finished tasks
- **--tags_any**: only show tasks with any of the specified tags
- **--tags_all**: only show tasks with at least all of the specified tags
- **--location**: only show tasks with any of the specified locations
### Example
```
$ bullet init

$ bullet new task Sample_Title This is a sample body

$ bullet new task
title: Sample_Prompted_Title
body: This is a sample prompted body

$ bullet set task 1 level 2

$ bullet set task 2 status 2

$ bullet tag 1 py sql

$ bullet new subtask 2 Sample_Subtask
body: This is a sample prompted subtask body

$ bullet show
○ (1) Sample_Title: This is a sample body
| {Normal}
| [py] [sql]
|
○ (2) Sample_Prompted_Title: This is a sample prompted body
| {In Progress}
|  |
|  ○ (1) Sample_Subtask: This is a sample prompted subtask body
|

$ bullet child 2 1

$ bullet show
○ (2) Sample_Prompted_Title: This is a sample prompted body
| {In Progress}
|  |
|  ○ (1) Sample_Subtask: This is a sample prompted subtask body
|

bullet show --all --tags_any py
○ (1) Sample_Title: This is a sample body
| {Normal}
| [py] [sql]
|
```
### Help Message
```
usage: bullet [--help|help]                                                     (0)
       bullet init                                                              (1)
       bullet new task [<title>] [<body>...]                                    (2)
       bullet new subtask <task_id> [<title>] [<body>...]                       (3)
       bullet delete (task|subtask) <bullet_id> [--confirm|confirm]             (4)
       bullet (<command>) <task_id> [<args>...]                                 (5)
       bullet set (task|subtask) <bullet_id> (<attribute>) <val>                (6)
       bullet show [--all|--relevant|--unfinished|--<filter> [<args>]...]...    (7)

(0) view this help message

(1) create a new bullet-backlog in this directory

(2) create a new task
    ○ if no arguments provided, title and body will be prompted
    ○ if only one argument <arg> is provided, title=<arg> and body will be prompted
    ex: bullet new task sample_title this is a sample body

(3) create a new subtask under task <task_id>
    ○ if no arguments provided, title and body will be prompted
    ○ if only one argument <arg> is provided, title=<arg> and body will be prompted
    ex: bullet new subtask 1

(4) delete an existing bullet
    ○ if confirmation not provided, confirmation will be prompted
    ex: bullet delete subtask 4 --confirm

(5) add relations/tags to an existing task <task_id>
    ○ commands: tag, untag, parent, unparent, child, unchild
    ○ tag: an attribute of a task
    ○ parent: if task <a> is a parent of task <b>, then <b> relies on <a>
    ○ child: if task <a> is a child of task <b>, then <a> relies on <b>
    ex: bullet tag 2 python sql cli

(6) edit attribute values for an existing bullet <bullet_id>
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

(7) visualize bullets in the terminal with stacking filters
    ○ filters: --all, --relevant, --unfinished, --tags_any, --tags_all, location
    ○ --all: show all tasks
    ○ --relevant: filter out tasks whose parents are not complete
    ○ --unfinished: filter out finished tasks
    ○ --tags_any: only show tasks with any of the specified tags
    ○ --tags_all: only show tasks with at least all of the specified tags
    ○ --location: only show tasks with any of the specified locations
```
