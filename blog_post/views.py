from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, DeleteView

from blog_post.forms import RegistrationForm, AddCommentForm, CreateEditPostForm, UserUpdateForm, ProfileUpdateForm
from blog_post.models import Post
from config import settings


# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True).order_by('-created_at')
    template_name = 'post_list.html'
    paginate_by = 10


class PostDetailView(LoginRequiredMixin, View):
    login_url = 'login-view'
    template_name = 'post_detail.html'
    form_class = AddCommentForm

    def setup(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'post': self.post,
            'comments': self.post.comment_set.all(),
            'tags': self.post.tag.all(),
            'form': self.form_class
        }
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
    form_class = CreateEditPostForm
    login_url = 'login-view'
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
            if form.cleaned_data['tag']:
                post.tag.set(form.cleaned_data['tag'])
                post.save()
            return redirect(post.get_absolute_url())
        else:
            context = {'form': form, 'errors': form.errors}
            return render(request, self.template_name, context)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    login_url = 'login-view'
    template_name = 'post_form.html'
    fields = ["title", "content", "image", "tag"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update
        return context

    def get_success_url(self, **kwargs):
        messages.success(
            self.request, 'Your post has been updated successfully.')
        return reverse_lazy('post_detail', slug=kwargs['slug'])

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    login_url = 'login-view'
    template_name = 'post_confirm_delete.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("home-page")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login-view'

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'profile.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('profile-view')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request, 'Error updating your profile')
            return render(request, 'profile.html', context)


class Login(LoginView):
    template_name = 'login.html'

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
        return settings.LOGIN_REDIRECT_URL


class Logout(LoginRequiredMixin, LogoutView):
    login_url = 'login-view'


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
