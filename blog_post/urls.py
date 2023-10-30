from .views import *
from django.urls import path

urlpatterns = [
    path('', PostListView.as_view(), name='home-page'),
    path('signup', SignupView.as_view(), name='signup-view'),
    path('login', Login.as_view(), name='login-view'),
    path('logout', Logout.as_view(), name='logout-view'),
    path('profile', ProfileView.as_view(), name='profile-view'),
    path('posts', CreatePostView.as_view(), name='create_post'),
    path('tags/<str:tag_name>/', TagPostsListView.as_view(), name='post-tags'),
    path('posts/<str:unique_id>/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('posts/<str:unique_id>/<slug:slug>/update', UpdatePostView.as_view(), name='post_update'),
    path('posts/<str:unique_id>/<slug:slug>/delete', DeletePostView.as_view(), name='post_delete'),
    path('posts/<str:unique_id>/<slug:slug>/like', like_post, name='like_post'),
    path('posts/<str:unique_id>/<slug:slug>/unlike', unlike_post, name='unlike_post'),
]
