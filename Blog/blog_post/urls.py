from .views import *
from django.urls import path

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('signup', SignupView.as_view(), name='signup-view'),
    path('login', Login.as_view(), name='login-view'),
    path('logout', logout_user, name='logout-view'),
    path('posts/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/like', like_post, name='like_post'),
    path('posts/<slug:slug>/unlike', unlike_post, name='unlike_post'),
    path('posts/<slug:slug>/add_comment', add_comment, name='add_comment'),
]
