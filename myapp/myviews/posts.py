from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from myapp.models import Post, User, LikesAndUsers
from .login import Login

class Posts:
    def __init__(self, request, page):
        self.request = request
        self.page = page
        self.context = {}

    def response(self):
        if self.request.method == 'POST':
            return self.post()
        else:
            return self.get()

    def post(self):
        if self.is_user_logged_on():
            try:
                return self.like()
            except Exception as e:
                return HttpResponse(str(e))
        else:
            return self.redirect_to_login()

    def get(self):
        self.prepare_context()
        return render(self.request, 'myapp/posts.html', self.context)
    
    def get_post_data(self):
            post_id = self.request.POST.get('id')
            user_id = self.request.session['user_id']
            return post_id, user_id

    def redirect_to_login(self):
        return HttpResponseRedirect(reverse('login'))

    def prepare_context(self):
        if self.page == 'new':
            self.context['active_new'] = 'active'
            self.context['posts'] = self.get_new_records()
        elif self.page == 'top':
            self.context['active_top'] = 'active'
            self.context['posts'] = self.get_top_records()
        if self.is_user_logged_on():
            user_id = self.request.session['user_id']
            self.context['liked_posts'] = self.posts_liked_by_user(user_id)

    def get_top_records(self):
        records = Post.objects.all().order_by('-point')
        return records

    def get_new_records(self):
        records = Post.objects.all().order_by('-id')
        return records
    
    def is_user_logged_on(self):
        return Login.is_user_logged_on(self.request, self.context)
    
    def posts_liked_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        posts_liked_by_user = []
        for obj in LikesAndUsers.objects.filter(user=user):
            posts_liked_by_user.append(obj.post.id)
        return posts_liked_by_user
    
    def get_post_and_user(self):
        post_id, user_id = self.get_post_data()
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=user_id) 
        return post, user

    def like(self):
        post, user = self.get_post_and_user()
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
