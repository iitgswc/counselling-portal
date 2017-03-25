from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from dost import settings
import time
from random import randint
from .models import Chat,counsallot,requests,ArchChat,notif
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
            c = Chat.objects.filter((Q(user=request.user)| Q(userto=request.user.username))&Q(labelc='old')).order_by('created')
            return render(request, "alpha/home.html", {'home': 'active', 'chat': c,'urls':urls})
        else:
            return redirect('/chat/mainhome')

@login_required
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        k=counsallot.objects.filter(username=request.user.username)
        if(k.exists()):
            c = Chat(user=request.user, message=msg,userto=k[0].counsname,label='new')
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
        c = Chat(user=request.user, message=msg,userto=username,labelc='new')
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
        c = Chat.objects.filter((Q(user=request.user) | Q(userto=request.user.username))&Q(labelc='new')).order_by('created')
        for ob in c:
            ob.labelc='old'
            ob.save()
        return render(request, 'alpha/messages.html', {'chat': c,'cond':True})

@login_required
def counsellorhome(request,id):
    if (request.user.is_staff == False):
        return HttpResponse('You are not authorized to see this')
    else:
        t = counsallot.objects.filter(counsname=request.user.username)
        if(User.objects.filter(username=id).exists()):
            if (t.exists() and t[0].username==id):
                user2=User.objects.get(username=id)
                c = Chat.objects.filter((Q(user=user2) | Q(userto=id))&Q(label='old')).order_by('created')
                url='/chat/counsarchive/'+id
                return render(request,'alpha/homecounsellor.html',{'chat':c,'username':id,'url':url})
            else:
                return redirect('/chat/mainhomecounsellor')
        else:
            return redirect('/chat/mainhomecounsellor')

@login_required
def Messages2(request):
    if (request.user.is_staff == False):
        return HttpResponse('You are not authorized to see this')
    else:
        if(User.objects.filter(username=request.GET['id']).exists()):
             user2=User.objects.get(username=request.GET['id'])
             c = Chat.objects.filter((Q(user=user2) | Q(userto=request.GET['id']))&Q(label='new')).order_by('created')
             for ob in c:
                 ob.label = 'old'
                 ob.save()
             return render(request, 'alpha/messages2.html', {'chat': c,'username':request.GET['id']})
        else:
            return redirect('/chat/mainhomecounsellor')

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
        r=requests.objects.filter(username=request.user.username)[0]
        if(r.status=='na'):
            r.delete()
            c=requests(username=request.user.username,status='na')
            c.save()
    else:
        c = requests(username=request.user.username, status='na')
        c.save()
    return redirect('/chat/mainhome')

@login_required
def mainhomecounsellor(request):
    if(request.user.is_staff==False):
        return HttpResponse("<h1>Not Authorized to accesss this page</h1>")
    else:
        c=requests.objects.all().order_by('-created');
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
        if(notif.objects.filter(Q(username=c[0].username),Q(counsname=request.user.username)).exists()):
            pass
        else:
            newob=notif(username=c[0].username,counsname=request.user.username,status="old")
            newob.save()
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
        if (notif.objects.filter(Q(username=c[0].username), Q(counsname=request.user.username)).exists()):
            pass
        else:
            newob = notif(username=c[0].username, counsname=request.user.username, status="old")
            newob.save()
    c[0].delete()
    return redirect('/chat/mainhomecounsellor')

@login_required
def archieve(request,id):
    if(request.user.is_staff==True):
        return HttpResponse('You are not authorized to access this page')
    else:
        if (User.objects.filter(username=id).exists()):
            user2=User.objects.get(username=id)
            chatlist=ArchChat.objects.filter((Q(userto=request.user.username)& Q(user=user2))|(Q(userto=id)& Q(user=request.user))).order_by('created')
            return render(request, 'alpha/archieve.html',
                          {'chat':chatlist,'post_url':'/chat/post3/'+id})
        else:
            return HttpResponse('Counsellor does not exist')

@login_required
def counsarchieve(request,id):
    if (request.user.is_staff == False):
        return HttpResponse('You are not authorized to access this page')
    else:
        if (User.objects.filter(username=id).exists()):
            user2 = User.objects.get(username=id)
            chatlist = ArchChat.objects.filter(
                (Q(userto=request.user.username) & Q(user=user2)) | (Q(userto=id) & Q(user=request.user))).order_by(
                'created')

            return render(request, 'alpha/counsarchieve.html',
                          {'chat': chatlist,'post_url':'/chat/post3/'+id})
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
        obj=notif.objects.filter(counsname=request.user.username)
        if (obj.exists()):
            t = set()
            s =set()
            for ob in obj:
                if(ob.status=="new"):
                    s.add(ob.username)
                else:
                    t.add(ob.username)
            urls = []
            for p in t:
                ob = k('/chat/counsarchive/' + p, p)
                urls.append(ob)
            newurls=[]
            for p in s:
                ob = k('/chat/makeold/' + p, p)
                newurls.append(ob)
            return render(request, 'alpha/allarchieve.html', {'urls': urls,'newurls': newurls})
        else:
            return HttpResponse('No Archived chats till now')

@login_required
def post3(request,id):
    if request.method == "POST":
        msg = request.POST.get('chat-msg')
        c = ArchChat(user=request.user, message=msg,userto=id)
        if msg != '':
            c.save()
            if (request.user.is_staff == False):
                if (notif.objects.filter(Q(username=request.user.username), Q(counsname=id)).exists()):
                    newob=notif.objects.filter(Q(username=request.user.username), Q(counsname=id))
                    obnew=newob[0]
                    obnew.status="new"
                    obnew.save()
                else:
                    newob = notif(username=request.user.username, counsname=id, status="new")
                    newob.save()
        if(request.user.is_staff==False):
            return redirect('/chat/archive/'+id)
        else:
            return redirect('/chat/counsarchive/' + id)
    else:
        return HttpResponse('Request must be POST.')

@login_required
def makeold(request,id):
    if(request.user.is_staff==False):
        return HttpResponse('Not Authorized to access this page')
    else:
        if (notif.objects.filter(Q(counsname=request.user.username), Q(username=id)).exists()):
            newob = notif.objects.filter(Q(counsname=request.user.username), Q(username=id))
            obnew=newob[0]
            obnew.status="old"
            obnew.save()
        return redirect('/chat/counsarchive/'+id)