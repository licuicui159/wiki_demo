from django.conf.urls import url

from user import views

urlpatterns = [
    # http://127.0.0.1:8000/user/test_celery
    url(r'^test_celery$', views.test_celery),

]
