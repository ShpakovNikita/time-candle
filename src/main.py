from adapters import task_adapter
from task import Task

# TODO: cut down lower part of the code from this module


def main():
    file = open('data.json', 'w+')
    created_task = Task.make_task(2018)
    print(created_task.__dict__)
    task_adapter.save(created_task)
    pass


if __name__ == "__main__":
    main()
