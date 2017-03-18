from django.conf.urls import url
from .import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', views.login_view),
     url(r'^$', views.forgot_password)

]