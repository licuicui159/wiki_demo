from django.conf.urls import url

from booking import views

urlpatterns = [

    # http://127.0.0.1:8000/v1/booking/order
    url(r'',views.order),
]