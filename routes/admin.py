from django.contrib import admin
from .models import Route, RouteImage
from .models import RouteCoordinate
admin.site.register(RouteCoordinate)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('created_at',)

@admin.register(RouteImage)
class RouteImageAdmin(admin.ModelAdmin):
    list_display = ('route', 'image')