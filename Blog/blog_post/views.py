from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from blog_post.models import Post, User, Follow


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


class Logout(LogoutView):
    pass


@login_required(login_url='/blog/login')
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/blog/login')
def follow_author(request, pk):
    author = get_object_or_404(User, pk=pk)
    if not Follow.objects.filter(follower=request.user, following=author).exists():
        Follow.objects.create(follower=request.user, following=author)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/blog/login')
def unfollow_author(request, pk):
    author = get_object_or_404(User, pk=pk)
    follow = get_object_or_404(Follow, follower=request.user, following=author)
    follow.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
