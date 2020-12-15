from threading import Lock, Thread

class SingletonMeta(type):
    """
    Abstraction of Singleton Thread safe 
    """

    _instance_list = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):

        with cls._lock:
            if cls not in cls._instance_list:
                new_instance = super().__call__(*args, **kwargs)
                cls._instance_list[cls] = new_instance

        return cls._instance_list[cls]