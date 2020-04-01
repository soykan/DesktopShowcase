from django.views.generic import View, TemplateView
from django.shortcuts import HttpResponseRedirect, render, HttpResponse
from django.urls import reverse
from myapp.models import Post, User, LikesAndUsers
from myapp.myviews.login import LoginView

class PostList(TemplateView):
    template_name = 'myapp/posts.html'
    ordering_column = ''
    active_menu = ''
    page = ''

    def post(self, request):
        context = self.get_context_data()
        if self.is_user_logged_on(context):
            return self.like()
        else:
            return self.redirect_to_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.active_menu] = 'active'
        context['posts'] = Post.objects.all().order_by(self.ordering_column)
        if self.is_user_logged_on(context):
            user_id = self.request.session['user_id']
            context['liked_posts'] = self.posts_liked_by_user(user_id)
        return context

    def posts_liked_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        posts_liked_by_user = []
        for obj in LikesAndUsers.objects.filter(user=user):
            posts_liked_by_user.append(obj.post.id)
        return posts_liked_by_user

    def is_user_logged_on(self, context):
        return LoginView.is_user_logged_on(self.request, context)

    def redirect_to_login(self):
        return HttpResponseRedirect(reverse('login'))
    
    def get_post_and_user(self):
        post_id, user_id = self.get_post_data()
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=user_id) 
        return post, user

    def get_post_data(self):
        post_id = self.request.POST.get('id')
        user_id = self.request.session['user_id']
        return post_id, user_id

    def like(self):
        try:
            post, user = self.get_post_and_user()
            like_obj = LikePost(post, user, self.page)
            return like_obj.like()
        except Exception as e:
            return HttpResponse(str(e))

class LikePost():
    def __init__(self, post, user, page):
        self.post = post
        self.user = user
        self.page = page
    
    def like(self):
        post, user = self.post, self.user
        try:
            self.unlike_post(post, user)
        except LikesAndUsers.DoesNotExist:            
            self.like_post(post, user)
        return HttpResponseRedirect(reverse(self.page))

    def unlike_post(self, post, user):
        record = LikesAndUsers.objects.get(post=post, user=user)
        record.delete()
        post.point = post.point - 1
        post.save()
    
    def like_post(self, post, user):
        post.point = post.point + 1
        post.save()
        record = LikesAndUsers(user=user, post=post)
        record.save()
