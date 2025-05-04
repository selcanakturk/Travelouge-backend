from django.urls import path, include
from routes import views
from routes.views import comments_list_create, log_search_view, public_route_list, route_list, route_detail ,toggle_like, comment_list_create, popular_routes, suggested_routes


urlpatterns = [
    path('routes/', views.route_list, name='route_list'),  # Tüm rotaları listele veya yeni rota ekle
    path('routes/<int:pk>/', views.route_detail, name='route_detail'),  # Belirli rotayı göster veya resim ekle
    path('routes/all/', public_route_list),
    path('routes/<int:pk>/like/', toggle_like, name='toggle_like'), 
    path('routes/<int:pk>/is-liked/', views.is_liked, name='is_liked'),
    path('routes/<int:pk>/comments/', comments_list_create, name='comments_list_create'),
    path('routes/<int:route_id>/comments/<int:comment_id>/', views.comment_detail, name='comment_detail'),
    path('routes/popular/', popular_routes, name='popular-routes'),
    path('routes/suggested/', views.suggested_routes, name='suggested_routes'),
    path('routes/search-log/', log_search_view),
    
]
