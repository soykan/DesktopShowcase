from django.views.generic import ListView
from myapp.models import Post
from myapp.myviews.post_list import PostList

class TopPostList(PostList):
    def __init__(self):
        self.ordering_column = '-point'
        self.active_menu = 'active_top'
        self.page = 'top'