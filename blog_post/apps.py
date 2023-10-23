from django.apps import AppConfig


class BlogPostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_post'

    def ready(self):
        import blog_post.signals
