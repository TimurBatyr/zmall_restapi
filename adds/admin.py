from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(City)
admin.site.register(Views)
admin.site.register(ViewsContact)
admin.site.register(PostContacts)
admin.site.register(Post)
admin.site.register(PostImages)
admin.site.register(Favorite)
admin.site.register(PostComplaint)

@admin.register(Subscription)
class SubscirptionAdmin(admin.ModelAdmin):
    list_display = ['choice', 'price',  'period']

@admin.register(ReviewPost)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["title", "email", 'text', "parent", "post", "id"]
    readonly_fields = ("title", "email")
