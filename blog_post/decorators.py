from functools import wraps

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from blog_post.models import Visit, Post
from blog_post.utils import get_client_ip


def track_visit(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        post_slug = kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug)

        response = function(request, *args, **kwargs)

        visit_identifier = request.request.COOKIES.get('visit_identifier')
        if not visit_identifier:
            visit_identifier = get_random_string(16)
            response.set_cookie('visit_identifier', visit_identifier)

        ip_address = get_client_ip(request.request)
        # Create or retrieve the Visit object
        visit = Visit.objects.filter(post=post).filter(
            Q(ip_address=ip_address) |
            Q(visit_identifier=visit_identifier) |
            Q(ip_address=ip_address, visit_identifier=visit_identifier)).first()

        if not visit:
            Visit.objects.create(post=post,
                                 visit_identifier=visit_identifier,
                                 ip_address=ip_address)
        return response

    return wrapper
