from .views import *
from django.urls import path

urlpatterns = [
    path('', PostListView.as_view(), name='home-page'),
    path('signup', SignupView.as_view(), name='signup-view'),
    path('login', Login.as_view(), name='login-view'),
    path('logout', Logout.as_view(), name='logout-view'),
    path('profile', ProfileView.as_view(), name='profile-view'),
    path('search', SearchView.as_view(), name='search'),
    path('tags/<str:tag_name>/', TagPostsListView.as_view(), name='post-tags'),
    path('posts', CreatePostView.as_view(), name='create_post'),
    path('posts/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/update', UpdatePostView.as_view(), name='post_update'),
    path('posts/<slug:slug>/delete', DeletePostView.as_view(), name='post_delete'),
    path('posts/<slug:slug>/like', like_post, name='like_post'),
    path('posts/<slug:slug>/unlike', unlike_post, name='unlike_post'),
]
