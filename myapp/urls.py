from django.urls import path

from . import views
from myapp.views import AboutView, IndexView, TopPostList, NewPostList, UploadView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # /myapp/
    path('', IndexView.as_view(), name='index'),
    path('new/', NewPostList.as_view(), name='new'),
    path('top/', views.top, name='top'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('about/', AboutView.as_view(), name='about'),
    path('top-post-list/', TopPostList.as_view(), name='top-post-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
