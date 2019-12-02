import datetime
from .tasks import task_test
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect

# Create your views here.

def test_celery(request):

    # 模拟worker将执行阻塞10秒左右任务
    task_test.delay()
    now = datetime.datetime.now()
    html = 'return at %s' % (now.strftime('%H-%M-%S'))
    return HttpResponse(html)