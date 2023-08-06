import time

from ngpuinfo import NGPUInfo

from fedflow.task.task import Task


class TaskScheduler(object):

    tasks = []
    loading_delay = 30
    default_memory = 2048

    @classmethod
    def start(cls):
        all_finished = False
        while not all_finished:
            all_finished = True
            for task in cls.tasks:
                if not task.is_finished():
                    all_finished = False
                    if not task.is_alive():
                        if cls.attempt_run_task(task):
                            time.sleep(cls.loading_delay)
            time.sleep(60)

    @classmethod
    def add_task(cls, task: Task):
        cls.tasks.append(task)

    @classmethod
    def attempt_run_task(cls, task: Task):
        cuda = cls.assign_cuda(task)
        if cuda == -2:
            return False
        task.cuda = cuda
        task.start()
        return True

    @classmethod
    def assign_cuda(cls, task: Task):
        cuda = -2
        if task.cuda is not None:
            cuda = task.cuda
        else:
            if task.estimate_memory is None:
                mem = cls.default_memory * 1024 * 1024
            else:
                mem = task.estimate_memory
            gpus = NGPUInfo.list_gpus()
            for i in range(1, len(gpus) + 1):
                g = gpus[-i]
                if g.mem_free() > mem:
                    cuda = g.id
                    break
        return cuda
