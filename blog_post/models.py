import os
import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from config import settings


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post-tags', kwargs={'tag_name': self.name})


def post_image_upload_path(instance, filename):
    return os.path.join('images', instance.slug, filename)


def generate_unique_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    unique_id = models.CharField(max_length=7, editable=False, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to=post_image_upload_path)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug, 'unique_id': self.unique_id})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.unique_id:
            self.unique_id = get_random_string(7)
        return super().save(*args, **kwargs)

    def get_visit_count(self):
        return Visit.objects.filter(post=self).count()


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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=profile_image_upload_path, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Visit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    visit_identifier = models.CharField(max_length=16)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.ip_address}:{self.visit_identifier}"
