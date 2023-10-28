from blog_post.models import Visit


def count_visits(func):
    def wrapper(request, *args, **kwargs):
        url = '/posts/' + kwargs['unique_id'] + '/' + kwargs['slug']
        visit, created = Visit.objects.get_or_create(url=url)
        visit.count += 1
        visit.save()
        response = func(request, *args, **kwargs)
        return response

    return wrapper
