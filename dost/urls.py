"""dost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import (login_view, logout_view, forgot_password)
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^', include("main.urls")),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^forgotpassword/', forgot_password, name='forgot_password'),

    url(r'^discussions/', include("discussions.urls", namespace='posts')),
    url('^register/', CreateView.as_view(
        template_name='register.html',
        form_class=UserCreationForm,
        success_url='/'
    )),
    url(r'^chat/',include('alpha.urls')),
    # url('^accounts/', include('django.contrib.auth.urls')),
    url('^quotes/', include('quotes.urls')),
    url('^team/', include('team.urls'))

]
