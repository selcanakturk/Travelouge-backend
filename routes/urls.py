from django.urls import path, include
from routes import views
from routes.views import route_list, route_detail  # route_create yerine route_list

# # Router tanımlaması
# router = DefaultRouter()
# router.register('routes', RouteViewSet)  # 'api/routes' için RouteViewSet kaydettik

urlpatterns = [
    path('routes/', views.route_list, name='route_list'),  # Tüm rotaları listele veya yeni rota ekle
    path('routes/<int:pk>/', views.route_detail, name='route_detail'),  # Belirli rotayı göster veya resim ekle
   # path('api/routes/', get_routes, name="get_routes"),
]
