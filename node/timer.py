import threading
import time


class Timer(threading.Timer):
    started_at = None

    def start(self):
        self.started_at = time.time()
        threading.Timer.start(self)

    def elapsed(self) -> float:
        return time.time() - self.started_at

    def remaining(self) -> float:
        rem = self.interval - self.elapsed()
        if rem > 0:
            return rem
        return 0.0
