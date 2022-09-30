from django.core.cache import cache


class FirstMiddleware:
    def __init__(self,get_response):
        self._get_response = get_response

    def __call__(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')
        else:
            ip = request.META.get('REMOTE_ADDR')

        print(ip)

        count = cache.get_or_set(f'ip:{ip}',0,30)
        count += 1
        if count > 1000:
            raise Exception('Джай Джай Джай не делай много запросов!')
        else:
            cache.set(f'ip:{ip}', count,30)

        response =self._get_response(request)
        return response