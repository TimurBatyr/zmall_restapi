from django.core.cache import cache


class FirstMiddleware:
    def __init__(self,get_response):
        self._get_response = get_response
        print('klai')

    def __call__(self,request):
        print(request.user.is_authenticated)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')
        else:
            ip = request.META.get('REMOTE_ADDR')


        print(ip)
        print('My first Middleware')

        # count = cache.get_or_set(f'ip:{ip}',0,30)
        # count += 1
        # if count > 4:
        #     raise Exception('Давай, - до свидания')
        # else:
        #     cache.set(f'ip:{ip}', count,30)

        response =self._get_response(request)
        return response
