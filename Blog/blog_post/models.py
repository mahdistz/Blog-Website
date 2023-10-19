import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


def image_upload_path(instance, filename):
    return os.path.join('images', instance.slug, filename)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    image = models.ImageField(blank=True, null=True, upload_to=image_upload_path)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name="liked_posts")

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
