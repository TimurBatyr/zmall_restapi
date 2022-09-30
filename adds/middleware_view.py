import datetime
from django.core.cache import cache
from rest_framework.generics import get_object_or_404
from adds.models import Post, Views


class ViewMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')
        else:
            ip = request.META.get('REMOTE_ADDR')
        count = cache.get_or_set(f'ip:{ip}', 0, 86400)
        count += 1
        path = request.path.split('/')
        date = datetime.datetime.now(tz=None)
        if not count != 2:
            if 'view' in path:
                val = path[-1]
                post = get_object_or_404(Post, pk=val)
                view_object = Views.objects.filter(post=post).filter(date=date).exists()
                if view_object == False:
                    Views.objects.create(post=post, date=date)
                post.views += 1
                post.save(update_fields=["views"])
                name = Views.objects.filter(post=post).filter(date=date).values('pk')
                name = Views.objects.get(pk=name[0]['pk'])
                name.date = date
                name.save(update_fields=["date"])
                name.views += 1
                name.save(update_fields=["views"])

        else:
            cache.set(f'ip:{ip}', count, 86400)
        response = self._get_response(request)
        return response