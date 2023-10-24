import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField

from config import settings


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def post_image_upload_path(instance, filename):
    return os.path.join('images', instance.slug, filename)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    image = models.ImageField(blank=True, null=True, upload_to=post_image_upload_path)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"

    @property
    def count_likes(self):
        return Like.objects.filter(post=self.post).count()


def profile_image_upload_path(instance, filename):
    return os.path.join('profiles', instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=profile_image_upload_path, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Visit(models.Model):
    url = models.URLField(max_length=255)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.url} - {self.count}"
