from django.urls import path

from . import views
from myapp.views import AboutView, IndexView, TopPostList, NewPostList, UploadView, LoginView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # /myapp/
    path('', IndexView.as_view(), name='index'),
    path('new/', NewPostList.as_view(), name='new'),
    path('top/', TopPostList.as_view(), name='top'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('about/', AboutView.as_view(), name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
