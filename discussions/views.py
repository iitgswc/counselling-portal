from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.http import HttpResponseRedirect
from .models import post
from .forms import post_form
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
from comment.models import comment



def index(request):
    return render(request, "discussions/practise.html")

def upvote(request,id):
    var = post.objects.get(pk=id)
    # result = could_return_none(var.score)
    # if result is None:
    #     result = DEFAULT_VALUE
    # result += 1
    var.score += 1
    var.save()
    return HttpResponse('/discussions/')


def post_detail(request, id):
    queryset = get_object_or_404(post, id=id)
    writer = queryset.writer

    # content_type = ContentType.objects.get_for_model(post)
    initial_data = {
        "content_type": queryset.get_content_type,
        "object_id": queryset.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if request.method == "POST":
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    if form.is_valid():
        # print(form.cleaned_data)
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        new_comment, created = comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data
        )

    comments = queryset.comments
    context = {
        "obj": queryset,
        "comments": comments,
        "comment_form": form,
        "writer": writer
    }
    return render(request, "discussions/post_detail.html", context)

def create_post(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    form = post_form(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.writer = request.user
        instance.save()
        return HttpResponseRedirect('/discussions')
    context = {
        "form": form
    }
    return render(request, "discussions/create_post.html", context)

def edit_post(request, id):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    instance = get_object_or_404(post, id=id)
    form = post_form(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_url_to_list())
    # else:
    #     messages.error(request, "Unsuccessful ")

    context = {
        "form": form
    }
    return render(request, "discussions/create_post.html", context)

# def search_post_list(request):



def post_list(request):
    instance_list = post.objects.all().order_by("-timestamp")

    search_query = request.GET.get("q")
    if search_query:
        instance_list = instance_list.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)| Q(option__icontains=search_query))
    paginator = Paginator(instance_list, 12)
    page = request.GET.get('page')
    try:
        instance = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        instance = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        instance = paginator.page(paginator.num_pages)
    context = {
        "instance": instance,
        "var": "var"
    }
    return render(request, "discussions/post_list.html", context)




def post_delete(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    var = get_object_or_404(post,id=id)
    var.delete()
    return redirect("posts:list")

