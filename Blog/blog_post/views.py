from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from blog_post.forms import RegistrationForm
from blog_post.models import Post, Comment


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
    success_url = 'post_list'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, error=form.errors))

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if next_page:
            return next_page
        return self.success_url


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


class SignupView(FormView):
    form_class = RegistrationForm
    template_name = 'signup.html'
    success_url = 'login'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name,
                      {'form': form, 'error': form.errors})


@login_required
def add_comment(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(post=post, author=request.user, content=content)
        return redirect('post_detail', slug=slug)
    else:
        return render(request, 'post_detail.html', {'post': post})
