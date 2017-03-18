from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ask/$', views.message1, name="message"),
    url(r'^messlist/$', views.messageList, name="messageList"),
    url(r'^messlist/(?P<id>\d+)/$', views.messageListDetail, name="detail"),
    url(r'^myinbox/$', views.myinbox, name="myinbox"),
    url(r'^myinbox/(?P<id>\d+)/$', views.myinboxDetail),
    url(r'^notifi/$', views.notifi),

]