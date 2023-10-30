from django.shortcuts import get_object_or_404

from blog_post.models import Visit, generate_unique_string, Post
from blog_post.utils import get_client_ip


def track_visit(function):
    def wrapper(request, *args, **kwargs):
        post_slug = kwargs.get('slug')
        post_unique_id = kwargs.get('unique_id')
        post = get_object_or_404(Post, slug=post_slug, unique_id=post_unique_id)
        response = function(request, *args, **kwargs)

        # Get the visit identifier from the cookie or create a new one
        visit_identifier = request.request.COOKIES.get('v')
        if not visit_identifier:
            visit_identifier = generate_unique_string(10)
            response.set_cookie('v', visit_identifier)

        # Check if the visit identifier and IP address combination has visited this article before
        ip_address = get_client_ip(request.request)
        if visit_identifier and ip_address:
            visit, created = Visit.objects.get_or_create(post=post,
                                                         visit_identifier=visit_identifier,
                                                         ip_address=ip_address)
            if created:
                # Increment visit count only if it's a new visit
                visit.count += 1
                visit.save()

        return response
    return wrapper
