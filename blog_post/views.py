from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, FormView

from blog_post.forms import RegistrationForm, AddCommentForm, CreatePostForm
from blog_post.models import Post, User


# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True).order_by('-created_at')
    template_name = 'post_list.html'
    paginate_by = 10


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'post_detail.html'
    form_class = AddCommentForm

    def setup(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post.comment_set.all()
        tags = self.post.tag.all()
        context = {'post': self.post, 'comments': comments, 'tags': tags, 'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=comment.post.slug)


class CreatePostView(LoginRequiredMixin, View):
    form_class = CreatePostForm
    template_name = 'create_post.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = True
            post.save()
            if form.cleaned_data['category']:
                post.category = form.cleaned_data['category']
                post.save()
            if form.cleaned_data['tag']:
                post.tag.set(form.cleaned_data['tag'])
                post.save()
            return redirect('post_detail', post.slug)
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form, 'errors': form.errors})


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
