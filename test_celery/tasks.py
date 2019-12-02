
#创建 tasks.py
from celery import Celery
app = Celery('guoxiaonao',
             broker='redis://:@127.0.0.1:6379/1')

# 创建任务函数
@app.task
def task_test():
    print("task is running...")
