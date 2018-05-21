def print_tasks(tasks):
    for task in tasks:
        print_task(task)


def print_task(task):
    print()
    print('Task ' + task.title)
    print('Task\'s id is ' + str(task.tid))
