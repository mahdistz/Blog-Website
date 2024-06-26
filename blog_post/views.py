from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, DeleteView, UpdateView

from blog_post.decorators import track_visit
from blog_post.forms import RegistrationForm, AddCommentForm, UserUpdateForm, ProfileUpdateForm, \
    CreatePostForm, UpdatePostForm
from blog_post.models import Post, Tag
from config import settings


# Create your views here.

def custom_404_view(request, exception):
    return HttpResponseNotFound(render(request, '404.html'))


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True)
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(LoginRequiredMixin, View):
    login_url = 'login-view'
    template_name = 'post_detail.html'
    form_class = AddCommentForm

    def setup(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    @track_visit
    def get(self, request, *args, **kwargs):
        context = {
            'post': self.object,
            'comments': self.object.comments.all(),
            'tags': self.object.tags.all(),
            'form': self.form_class,
            'visit_count': self.object.get_visits_count()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect(self.object.get_absolute_url())
        else:
            return render(request, self.template_name, {'form': form})


class CreatePostView(LoginRequiredMixin, View):
    form_class = CreatePostForm
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
            if form.cleaned_data['tags']:
                post.tags.set(form.cleaned_data['tags'])
                post.save()
            messages.success(request, 'Post created successfully')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, 'Error creating post')
            return render(request, self.template_name, {'form': form})


class UpdatePostView(LoginRequiredMixin, UpdateView):
    form_class = UpdatePostForm
    login_url = 'login-view'
    template_name = 'update_post.html'

    def setup(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, {'form': form, 'post': self.object})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            post = form.save(commit=False)
            if form.cleaned_data['tags']:
                post.tags.set(form.cleaned_data['tags'])
            post.save()
            messages.success(request, 'Post updated successfully')
            return redirect(self.object.get_absolute_url())
        else:
            messages.error(request, 'Error updating post')
            return render(request, self.template_name, {'form': form, 'post': self.object})


class DeletePostView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    login_url = 'login-view'
    template_name = 'post_confirm_delete.html'
    success_message = "Your post has been deleted successfully"

    def get_success_url(self):
        return reverse_lazy("home-page")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login-view'
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)

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
            return render(request, self.template_name, context)


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
        messages.error(self.request, 'Invalid username or password')
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


class SignupView(SuccessMessageMixin, FormView):
    form_class = RegistrationForm
    template_name = 'signup.html'
    success_url = 'login'
    success_message = 'Your account has been created successfully'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error creating your account')
        return render(self.request, self.template_name, {'form': form, 'error': form.errors})


class TagPostsListView(ListView):
    model = Tag
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, name=tag_name)
        queryset = tag.posts.filter(published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, name=tag_name)
        context['tag'] = tag
        return context


class SearchView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            post_result = Post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
            result = post_result
        else:
            result = None
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['search'] = query
        return context
