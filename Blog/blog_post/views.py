from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from blog_post.models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True).order_by('-created_at')
    template_name = 'post_list.html'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.filter(published=True)
    template_name = 'post_detail.html'


class Login(LoginView):
    template_name = 'login.html'

    def setup(self, request, *args, **kwargs):
        self.next_page = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if self.next_page:
                return redirect(self.next_page)
            else:
                return redirect('post_list')
        else:
            return render(request, self.template_name, {'error': 'Invalid username or password'})


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.liked_by.add(request.user)
    return redirect(post.get_absolute_url())


@login_required
def unlike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.liked_by.remove(request.user)
    return redirect(post.get_absolute_url())


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
