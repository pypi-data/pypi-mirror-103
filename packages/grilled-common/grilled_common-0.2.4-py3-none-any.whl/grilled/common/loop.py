import asyncio
from asyncio import AbstractEventLoop
from threading import Lock, Thread
from queue import Queue
from typing import Coroutine, Generator, Iterable, Tuple, Union, Dict


class LoopManagerMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class LoopManager(metaclass=LoopManagerMeta):
    _loops = {}  # {"ThreadName": loop object}

    def start_new_loop(self, thread_name):
        new_loop = asyncio.new_event_loop()
        task_queue = Queue()

        def new_thread(new_loop: AbstractEventLoop, task_queue: Queue):
            asyncio.set_event_loop(new_loop)

            async def main(task_queue: Queue):
                while True:
                    task = task_queue.get()
                    if task is not None:
                        new_loop.create_task(task)
                    task_queue.task_done()
                    await asyncio.sleep(0.1)

            new_loop.run_until_complete(main(task_queue))

        new_thread = Thread(
            target=new_thread,
            args=(new_loop, task_queue),
            name=thread_name,
        )
        new_thread.setDaemon(True)
        new_thread.start()
        return new_thread, new_loop, task_queue

    def new_event_loop(
        self, thread_name: Union[str, Iterable[str]] = None
    ) -> AbstractEventLoop:
        if isinstance(thread_name, str):
            new_thread, new_loop, task_queue = self.start_new_loop(thread_name)
            self._loops.update({new_thread.getName(): (new_loop, task_queue)})
            return new_loop, task_queue
        elif isinstance(thread_name, Iterable):
            new_loops = {
                new_thread.getName(): (new_loop, task_queue)
                for new_thread, new_loop, task_queue in (
                    self.start_new_loop(single_name) for single_name in thread_name
                )
            }
            self._loops.update(new_loops)
            return new_loops
        else:
            raise TypeError("Param thread_name must be str or iterable type.")

    def get_event_loop(
        self, thread_name=None
    ) -> Union[
        Dict[str, Tuple[AbstractEventLoop, Queue]], Tuple[AbstractEventLoop, Queue]
    ]:
        if thread_name is None:
            return self._loops
        else:
            return self._loops.get(thread_name)

    def create_task(
        self, task: Union[Coroutine, Generator], thread_name: str = None
    ) -> None:
        if (not isinstance(task, Coroutine)) and (not isinstance(task, Generator)):
            raise TypeError("Param task must be a Coroutine type.")
        if thread_name is None:
            loop = asyncio.get_event_loop()
            loop.create_task(task)
        else:
            if (loop_package := self._loops.get(thread_name)) is not None:
                loop, loop_queue = loop_package
                loop_queue.put(task)
            else:
                raise RuntimeError(
                    "Parma thread_name has not registed in loop manager."
                )
