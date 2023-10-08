import os
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField


# Create your models here.

class User(AbstractUser):
    pass

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_posts(self):
        return self.post_set.all()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def image_upload_path(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    unique_filename = uuid4().hex
    return f"images/{unique_filename}{file_extension}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    image = models.ImageField(blank=True, null=True, upload_to=image_upload_path)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
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


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
