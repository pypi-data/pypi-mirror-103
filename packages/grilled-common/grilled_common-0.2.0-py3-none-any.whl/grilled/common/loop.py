import asyncio
from asyncio import AbstractEventLoop
from threading import Lock, Thread


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

        def new_thread(new_loop: AbstractEventLoop):
            asyncio.set_event_loop(new_loop)
            new_loop.run_forever()

        new_thread = Thread(target=new_thread, args=(new_loop,), name=thread_name,)
        new_thread.setDaemon(True)
        new_thread.start()
        return new_thread, new_loop

    def new_event_loop(self, thread_name: str = None) -> AbstractEventLoop:
        new_thread, new_loop = self.start_new_loop(thread_name)
        self._loops.update({new_thread.getName(): new_loop})
        return new_loop

    def get_event_loop(self, thread_name=None):
        if thread_name is None:
            return self._loops
        else:
            return self._loops.get(thread_name)

