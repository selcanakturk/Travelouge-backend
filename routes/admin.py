from django.contrib import admin
from .models import Route, RouteImage, RouteCoordinate, Like, Comment
admin.site.register(RouteCoordinate)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('created_at',)

@admin.register(RouteImage)
class RouteImageAdmin(admin.ModelAdmin):
    list_display = ('route', 'image')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'text', 'created_at')
    search_fields = ('user__username', 'route__title', 'text')
    list_filter = ('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'created_at')
    search_fields = ('user__username', 'route__title')
    list_filter = ('created_at',)