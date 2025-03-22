from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import route_create

# # Router tanımlaması
# router = DefaultRouter()
# router.register('routes', RouteViewSet)  # 'api/routes' için RouteViewSet kaydettik

urlpatterns = [
   path('routes/', route_create, name='route-create'),  # Tüm URL'leri include ettik
]
