from celery import Celery
app = Celery('demo',
             broker='redis://@127.0.0.1:6379/1',
             backend='redis://@127.0.0.1:6379/2',)

@app.task()
def test_task_result(a,b):
    print('task is running')
    return a+b

