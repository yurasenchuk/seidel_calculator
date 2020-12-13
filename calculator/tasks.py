from celery import shared_task
from celery_progress.backend import ProgressRecorder

from calculator.models import Calculator
import time


@shared_task(bind=True)
def calculate_seidel_task(self, calculator_id):
    progress_recorder = ProgressRecorder(self)
    calculator = Calculator.get_by_id(calculator_id)
    x = calculator.calculate_seidel()
    if not x:
        for i in range(50):
            time.sleep(1)
            progress_recorder.set_progress((i + 1) * 2, 100, description="Calculating...")
        calculator.update(["No answer" for i in range(calculator.size)])
        return f"This task has no answer!!!"
    else:
        for i in range(100):
            time.sleep(1)
            progress_recorder.set_progress(i + 1, 100, description="Calculating...")
        calculator.update(x)
        return f"Result: x = {x}"
