from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.chat,name='chat'),
    url(r'^home/$', views.Home, name='home'),
    url(r'^home/(?P<id>[a-z,0-9]+)$', views.counsellorhome, name='counsellorhome'),
    url(r'^post/$', views.Post, name='post'),
    url(r'^post2/$', views.Post2, name='post2'),
    url(r'^messages/$', views.Messages, name='messages'),
    url(r'^messages2/', views.Messages2, name='messages2'),
    url(r'^mainhome/$',views.mainhome,name='mainhome'),
    url(r'^createrequest/$', views.createrequest, name='createrequest'),
    url(r'^mainhomecounsellor/$',views.mainhomecounsellor,name='mainhomecounsellor'),
    url(r'^allot/(?P<id>[a-z,0-9]+)', views.allot, name='allot'),
    url(r'^pause/$', views.pause, name='pause'),
    url(r'^complete/$', views.complete, name='complete'),
    url(r'^archive/(?P<id>[a-z,0-9]+)', views.archieve, name='archieve'),
    url(r'^check/$', views.check, name='check'),
    url(r'^counsarchive/(?P<id>[a-z,0-9]+)', views.counsarchieve, name='counsarchieve'),
    url(r'^allarchive/$', views.allarchieve, name='allarchieve')

]