from .views import *
from django.urls import path

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('signup', signup_view, name='signup-view'),
    path('login', Login.as_view(), name='login-view'),
    path('logout', logout_user, name='logout-view'),
    path('post/like/<slug:slug>', like_post, name='like_post'),
    path('post/unlike/<slug:slug>', unlike_post, name='unlike_post'),
    path('post/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
]
