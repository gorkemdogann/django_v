from django.contrib import admin

from .models import *

class AdminPost(admin.ModelAdmin):
    list_filter = ['date']
    list_display = ['title','date','user'] # burası admin panelindeki gösterimler
    search_fields = ['title','content','user']

    class Meta:
        model = Post


admin.site.register(Post,AdminPost)
admin.site.register(Category)
admin.site.register(Tag)
