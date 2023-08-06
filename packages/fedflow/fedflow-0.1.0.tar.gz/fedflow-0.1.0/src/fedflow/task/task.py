import abc
import uuid
import os
from enum import Enum
from multiprocessing import Process

from fedflow.context import WorkDirContext


class Task(object):

    class Status(Enum):
        AVAILABLE = 0
        RUNNING = 1
        FINISHED = 2

    def __init__(self, task_id: str = None, estimate_memory: int = None, cuda: int = None):
        """

        :param task_id: task id, use uuid if not specified
        :param estimate_memory: the max estimate memory of this task, unit is B
        :param cuda: zero-based gpu index(-1 if use cpu)
        """
        super(Task, self).__init__()
        self.task_id = task_id if task_id is not None else str(uuid.uuid4())
        self.process = Process(target=self.outer_run)
        self.estimate_memory = estimate_memory
        self.cuda = cuda
        self.has_run = False

    def start(self):
        self.has_run = True
        self.process.start()

    def outer_run(self):
        print("Task start: %s" % self.task_id)
        os.makedirs(self.task_id, exist_ok=True)
        with WorkDirContext(self.task_id):
            self.run()
        print("Task end  : %s" % self.task_id)

    @abc.abstractmethod
    def run(self):
        pass

    def join(self):
        self.process.join()

    def is_alive(self):
        return self.process.is_alive()

    def is_finished(self):
        return self.has_run and not self.process.is_alive()

    def device(self):
        if self.cuda < 0:
            return "cpu"
        else:
            return "cuda:%d" % self.cuda
