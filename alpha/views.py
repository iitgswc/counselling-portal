from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from dost import settings
import time
from random import randint
from .models import Chat,counsallot,requests,ArchChat
from django.contrib.auth.decorators import login_required


class k:
    url=""
    name=""

    def __init__(self, url, name):
        self.name = name
        self.url=url

@login_required
def chat(request):
    if(request.user.is_staff==True):
        return redirect('/chat/mainhomecounsellor')
    else:
        return redirect('/chat/mainhome')

@login_required
def Home(request):
    if (request.user.is_staff == True):
        return HttpResponse('You are not authorized to see this')
    else:
        t = counsallot.objects.filter(username=request.user.username)
        if (t.exists()):
            r=User.objects.filter(is_staff=True)
            urls=[]
            for ob in r:
                if(ob.is_superuser==False):
                    obt = k('/chat/archive/' + ob.username, ob.username)
                    urls.append(obt)
            c = Chat.objects.all()
            return render(request, "alpha/home.html", {'home': 'active', 'chat': c,'urls':urls})
        else:
            return redirect('/chat/mainhome')

@login_required
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        k=counsallot.objects.filter(username=request.user.username)
        if(k.exists()):
            c = Chat(user=request.user, message=msg,userto=k[0].counsname)
            if msg != '':
                c.save()
            return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

@login_required
def Post2(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        username = request.POST.get('username', None)
        c = Chat(user=request.user, message=msg,userto=username)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

@login_required
def Messages(request):
    if(request.user.is_staff==True):
        return HttpResponse('You are not authorized to see this')
    else:
        c = Chat.objects.all()
        return render(request, 'alpha/messages.html', {'chat': c,'cond':True})

@login_required
def counsellorhome(request,id):
    if (request.user.is_staff == False):
        return HttpResponse('You are not authorized to see this')
    else:
        t = counsallot.objects.filter(counsname=request.user.username)
        if (t.exists() and t[0].username==id):
            c = Chat.objects.all()
            url='/chat/counsarchive/'+id
            return render(request,'alpha/homecounsellor.html',{'chat':c,'username':id,'url':url})
        else:
            return redirect('/chat/mainhomecounsellor')

@login_required
def Messages2(request):
    if (request.user.is_staff == False):
        return HttpResponse('You are not authorized to see this')
    else:
        c = Chat.objects.all()
        return render(request, 'alpha/messages2.html', {'chat': c,'username':request.GET['id']})

@login_required
def mainhome(request):
    if (request.user.is_staff == True):
        return HttpResponse('Not Authorized to accesss this page')
    else:
        couns=counsallot.objects.filter(username=request.user.username)
        if (couns.exists()):
            urls=[]
            r = User.objects.filter(is_staff=True)
            for ob in r:
                if (ob.is_superuser == False):
                    obt = k('/chat/archive/' + ob.username, ob.username)
                    urls.append(obt)
            return render(request,'alpha/mainhome.html',{'cond':True,'urls':urls})
        else:
            req=requests.objects.filter(username=request.user.username)
            urls=[]
            r = User.objects.filter(is_staff=True)
            for ob in r:
                if (ob.is_superuser == False):
                    obt = k('/chat/archive/' + ob.username, ob.username)
                    urls.append(obt)
            if(req.exists()):
                return render(request, 'alpha/mainhome.html', {'cond': False,'cond2':True,'urls':urls})
            else:
                return render(request, 'alpha/mainhome.html', {'cond': False,'cond2':False,'urls':urls})

@login_required
def createrequest(request):
    if(request.user.is_staff==True):
        return HttpResponse('Not Authorized to visit this page')
    if (requests.objects.filter(username=request.user.username).exists()):
        return redirect('/chat/mainhome')
    c=requests(username=request.user.username,status='na')
    c.save()
    return redirect('/chat/mainhome')

@login_required
def mainhomecounsellor(request):
    if(request.user.is_staff==False):
        return HttpResponse("<h1>Not Authorized to accesss this page</h1>")
    else:
        c=requests.objects.all();
        for obj in c:
            if(obj.status=='completed'):
                obj.delete()

        couns=counsallot.objects.filter(counsname=request.user.username)
        if(couns.exists()):
            return render(request, 'alpha/mainhomecounsellor.html', {'cond': True,'url':'/chat/home/'+couns[0].username})
        else:
            urls=[]

            for obj in c:
                if(obj.status=='na'):
                    ob=k('/chat/allot/' + obj.username,obj.username)
                    urls.append(ob)
            return render(request, 'alpha/mainhomecounsellor.html',
                          {'cond': False, 'urls': urls})

@login_required
def allot(request,id):
    if(request.user.is_staff==False):
        return HttpResponse('Not Authorized to visit the page')
    all=counsallot.objects.filter(username=id)
    all2 = counsallot.objects.filter(counsname=request.user.username)
    if(requests.objects.filter(username=id).exists()):
        if(all.exists() or all2.exists() ):
            return redirect('/chat/mainhomecounsellor')
        else:
            c=counsallot(username=id,counsname=request.user.username)
            c.save()
            r=requests.objects.filter(username=id)
            p=r[0];
            p.status='alloted'
            p.save()
            return redirect('/chat/home/'+id)
    else:
        return redirect('/chat/mainhomecounsellor')


@login_required
def pause(request):
    if (request.user.is_staff == False):
        return HttpResponse('Not Authorized to visit the page')
    c=counsallot.objects.filter(counsname=request.user.username)
    t=counsallot.objects.filter(username=c[0].username).count()
    if(t==1):
        r = requests.objects.filter(username=c[0].username)
        p = r[0];
        p.status='na'
        p.save()
        obj = Chat.objects.all()
        for ob in obj:
            if (ob.user.username == c[0].username or ob.userto == c[0].username):
                k = ArchChat(user=ob.user, userto=ob.userto, message=ob.message)
                k.save()
                ob.delete()
    c[0].delete()
    return redirect('/chat/mainhomecounsellor')

@login_required
def complete(request):
    if (request.user.is_staff == False):
        return HttpResponse('Not Authorized to visit the page')
    c = counsallot.objects.filter(counsname=request.user.username)
    r = requests.objects.filter(username=c[0].username)
    t = counsallot.objects.filter(username=c[0].username).count()
    if (t == 1):
        p = r[0];
        p.status = 'completed'
        p.save()
        obj=Chat.objects.all()
        for ob in obj:
            if(ob.user.username==c[0].username or ob.userto==c[0].username):
                k=ArchChat(user=ob.user,userto=ob.userto,message=ob.message)
                k.save()
                ob.delete()
    c[0].delete()
    return redirect('/chat/mainhomecounsellor')

@login_required
def archieve(request,id):
    if(request.user.is_staff==True):
        return HttpResponse('You are not authorized to access this page')
    else:
        if (User.objects.filter(username=id).exists()):
            chat=ArchChat.objects.all()
            chatlist=[]
            for obj in chat:
                if(obj.userto==id and obj.user.username==request.user.username):
                    chatlist.append(obj)
                if (obj.userto == request.user.username and obj.user.username == id):
                    chatlist.append(obj)
            return render(request, 'alpha/archieve.html',
                          {'chat':chatlist})
        else:
            return HttpResponse('Counsellor does not exist')

@login_required
def counsarchieve(request,id):
    if (request.user.is_staff == False):
        return HttpResponse('You are not authorized to access this page')
    else:
        if (User.objects.filter(username=id).exists()):
            chat = ArchChat.objects.all()
            chatlist = []
            for obj in chat:
                if (obj.userto == id and obj.user.username == request.user.username):
                    chatlist.append(obj)
                if (obj.userto == request.user.username and obj.user.username == id):
                    chatlist.append(obj)
            return render(request, 'alpha/counsarchieve.html',
                          {'chat': chatlist})
        else:
            return HttpResponse('User does not exist')


@login_required
def check(request):
    if (request.user.is_staff == True):
        return HttpResponse('Not Authorized to visit the page')
    k = counsallot.objects.filter(username=request.user.username)
    if (k.exists()):
        return JsonResponse({ 'msg': 'Success'})
    else:
        return JsonResponse({'msg': 'Bye'})

@login_required
def allarchieve(request):
    if (request.user.is_staff==False):
        return HttpResponse('Not Authorized to visit the page')
    else:
        obj=ArchChat.objects.filter(user=request.user)
        if (obj.exists()):
            t = set()
            for ob in obj:
                t.add(ob.userto)
            urls = []
            for p in t:
                ob = k('/chat/counsarchive/' + p, p)
                urls.append(ob)
            return render(request, 'alpha/allarchieve.html', {'urls': urls})
        else:
            return HttpResponse('No Archived chats till now')