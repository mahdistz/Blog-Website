from .views import *
from django.urls import path

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('signup/', signup_view, name='signup-view'),
    path('login', Login.as_view(), name='login-view'),
    path('logout', Logout.as_view(), name='logout-view'),
    path('like_post/<int:pk>/', like_post, name='like_post'),
    path('follow_author/<int:pk>/', follow_author, name='follow_author'),
    path('unfollow_author/<int:pk>/', unfollow_author, name='unfollow_author'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
