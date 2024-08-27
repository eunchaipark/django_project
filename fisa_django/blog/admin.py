from django.contrib import admin
from .models import Post, comment, Tag
# Register your models here.
admin.site.register(Post)
admin.site.register(comment)
admin.site.register(Tag)