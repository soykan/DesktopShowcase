from django.views.generic import ListView
from myapp.models import Post

class TopPostList(ListView):
    template_name = 'myapp/top_post_list.html'
    model = Post
    ordering = '-point'
    context_object_name = 'post_list'