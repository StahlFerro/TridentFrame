import time


class CommandDiagnostics:
    def __init__(self):
        self.time_start = 0
        self.time_end = 0
        self.total_elapsed_time = self.time_end - self.time_start

    def start(self):
        self.time_start = time.time()

    def end(self):
        self.time_end = time.time()
        self.total_elapsed_time = self.time_end - self.time_start

