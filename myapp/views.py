from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .myviews.login import Login
from .myviews.posts import Posts
from .myviews.register import Register
from .myviews.about import AboutView
from .myviews.index import IndexView
from .myviews.top_post_list import TopPostList
from .myviews.new_post_list import NewPostList
from .myviews.upload import UploadView

def register(request):
    return Register(request).response()

def login(request):
    return Login(request).response()

def top(request):
    return Posts(request, 'top').response()

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('index'))

