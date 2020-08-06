import typing
import os


def detect_tasks(root_dirpath: str) -> tuple:
    """
    Detect Celery tasks from a root directory
    """
    tasks = []
    file_path = os.path.join(root_dirpath)
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if os.path.basename(root) == "tasks":
                if filename != "__init__.py" and filename.endswith(".py"):
                    task = (
                        os.path.join(root, filename)
                        .replace(root_dirpath + "/", "")
                        .replace("/", ".")
                        .replace(".py", "")
                    )
                    tasks.append(task)
    return tuple(tasks)


def detect_periodic_tasks(root_dirpath: str) -> typing.Dict:
    """
    Detect Celery periodic tasks from a root directory
    """
    tasks = {}
    file_path = os.path.join(root_dirpath)
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if os.path.basename(root) == "tasks":
                if filename.startswith("periodic_tasks"):
                    full_path = os.path.join(root, filename)
                    ldict = locals()
                    exec(open(full_path).read(), globals(), ldict)
                    try:
                        tasks.update(ldict["periodic_tasks"])
                    except NameError:
                        pass
    return tasks


class RetriableTaskException(Exception):
    """
    Exception for celery tasks that indicates task can be retried
    """

    pass


class UnRetriableTaskException(Exception):
    """
    Exception for celery tasks that indicates task cannot be retried
    """

    pass
