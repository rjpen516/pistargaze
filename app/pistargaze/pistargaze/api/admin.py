from django.contrib import admin

from .models import Photo, Session, Stars

# Register your models here.


admin.site.register(Photo)
admin.site.register(Session)
admin.site.register(Stars)