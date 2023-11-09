from django.db.models import Count

from blog_post.models import Post


def most_liked_posts_context_processor(request):
    return {
        'most_liked_posts': Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5],
    }


def most_visited_posts_context_processor(request):
    return {
        'most_visited_posts': Post.objects.annotate(visit_count=Count('visits')).order_by('-visit_count')[:5]
    }
