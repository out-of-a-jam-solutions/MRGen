# sheldon woodward
# jan 8, 2019

import time

from MRGen.celery import app


@app.task
def add(x, y):
    time.sleep(10)
    return x + y
