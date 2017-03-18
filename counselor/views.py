from django.http import HttpResponse, HttpResponseRedirect
from .forms import mess_to_couns
from .models import message, reply, notifications
from .forms import reply_form
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from discussions.models import notifications1
from .active_users import is_counselor1_online



def notifi(request):
    notifi1 = notifications.objects.all().order_by("-timestamp")
    notifi2 = notifications1.objects.all().order_by("-timestamp")

    context = {
        "notifi": notifi1,
        "notifi1":notifi2
    }
    return render(request, "counselor/notifications.html", context)


def message1(request):
    form = mess_to_couns(request.POST or None)
    online = is_counselor1_online()
    if form.is_valid():
        instance = form.save(commit=False)
        instance.writer = request.user
        instance.save()
        return HttpResponseRedirect('/counsellor/myinbox')
    context = {
        "form": form,
        "online" : online
    }
    return render(request, "counselor/mess_to_couns.html", context)

def myinbox(request):
    current_user = request.user
    queryset = message.objects.filter(writer=current_user).order_by("-timestamp")

    context = {
        "queryset": queryset,
        "user": current_user
    }
    return render(request, "counselor/my_inbox.html", context)
def myinboxDetail(request,id):
    queryset = reply.objects.filter(object_id=id)
    form = reply_form(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.object_id = id
        instance.save()
        # messages.success(request, "Successfully created")
        return HttpResponseRedirect('/counselor/myinbox/')

    context = {
        "queryset": queryset,
        "form": form
    }
    return render(request, "counselor/my_inbox_detail.html", context)

def messageList(request):
    queryset = message.objects.all().order_by("-timestamp")
    context = {
        "queryset": queryset
    }
    return render(request, "counselor/messList.html", context)

def messageListDetail(request, id):
    queryset = get_object_or_404(message, id=id)
    queryset2 = reply.objects.filter(object_id=id)
    form = reply_form(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.object_id = id
        instance.save()
        # messages.success(request, "Successfully created")
        return HttpResponseRedirect('/counselor/messlist/')

    context = {
        "obj": queryset,
        "form": form,
        "obj2": queryset2
    }
    return render(request, "counselor/messListDetail.html", context)





















