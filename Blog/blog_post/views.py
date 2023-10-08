from django.views.generic import ListView, DetailView

from blog_post.models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True).order_by('-created_at')
    template_name = 'blog_post/index.html'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.filter(published=True)
    template_name = 'blog_post/post_detail.html'
