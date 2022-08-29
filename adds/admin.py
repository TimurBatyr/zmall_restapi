from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(City)
admin.site.register(PhonePost)
admin.site.register(Post)
admin.site.register(Views)
admin.site.register(PostImages)
admin.site.register(Favorite)
admin.site.register(Subscription)