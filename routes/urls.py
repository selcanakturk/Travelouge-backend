from django.urls import path
from .views import (
    RouteListCreateView, RouteDetailView, AddRouteLocationView,
    UploadRouteImageView, CommentView, LikeView
)

urlpatterns = [
    # Rota listeleme ve oluşturma
    path('routes/', RouteListCreateView.as_view(), name='route_list_create'),
    # Belirli bir rotanın detaylarını görüntüleme, güncelleme ve silme
    path('routes/<int:pk>/', RouteDetailView.as_view(), name='route_detail'),
    # Belirli bir rotaya konum ekleme
    path('routes/<int:pk>/locations/', AddRouteLocationView.as_view(), name='add_location'),
    # Belirli bir rotaya resim yükleme
    path('routes/<int:pk>/upload-image/', UploadRouteImageView.as_view(), name='upload_image'),
    # Belirli bir rotaya yorum ekleme ve yorumları listeleme
    path('routes/<int:pk>/comments/', CommentView.as_view(), name='add_comment'),
    # Belirli bir rotaya beğeni ekleme/kaldırma
    path('routes/<int:pk>/like/', LikeView.as_view(), name='like_route'),
]
