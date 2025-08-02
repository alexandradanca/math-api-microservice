
import threading
import queue
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from controllers.math_controller import MathController

class MathWorker:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.results = []
        self.controller = MathController()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def add_task(self, operation, input_data):
        self.task_queue.put((operation, input_data))

    def _worker(self):
        while True:
            operation, input_data = self.task_queue.get()
            try:
                req = self.controller.process_request(operation, input_data)
                self.results.append(req)
            except Exception as e:
                self.results.append(str(e))
            self.task_queue.task_done()

    def get_results(self):
        return self.results
