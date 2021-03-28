from django.contrib import admin

# Register your models here.
from .models import Post, Profile, Photo, Video

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Video)
