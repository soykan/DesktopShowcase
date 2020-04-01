from django.views.generic import ListView
from myapp.models import Post
from myapp.myviews.post_list import PostList

class NewPostList(PostList):
    def __init__(self):
        self.ordering_column = '-id'
        self.active_menu = 'active_new'
        self.page = 'new'