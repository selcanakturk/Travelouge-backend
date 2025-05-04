from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from routes.models import Route, RouteCoordinate, RouteImage, Like, Comment, SearchLog, ViewedRoute
from routes.serializers import RouteSerializer, RouteImageSerializer, LikeSerializer, CommentSerializer
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models.functions import Random 
import json
import random

def log_search_term(user, term):
    if user.is_authenticated and term.strip():
        SearchLog.objects.create(user=user, term=term.strip().lower())

def get_top_search_terms(user, limit=3):
    return (
        SearchLog.objects
        .filter(user=user)
        .values('term')
        .annotate(count=Count('term'))
        .order_by('-count')[:limit]
    )

from routes.models import ViewedRoute

def get_viewed_titles(user, limit=3):
    viewed = ViewedRoute.objects.filter(user=user).select_related('route').order_by('-viewed_at')
    titles = [v.route.title for v in viewed if v.route and v.route.title]
    return titles[:limit]

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def route_list(request):
    if request.method == 'GET':
        routes = Route.objects.filter(user=request.user)
        serializer = RouteSerializer(routes, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RouteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            route = serializer.save(user=request.user)

            coordinates_json = request.data.get('coordinates', '[]')
            try:
                coordinates = json.loads(coordinates_json)
            except json.JSONDecodeError:
                coordinates = []

            for coord in coordinates:
                RouteCoordinate.objects.create(
                    route=route,
                    latitude=coord.get("latitude"),
                    longitude=coord.get("longitude")
                )

            for image_file in request.FILES.getlist('images'):
                RouteImage.objects.create(route=route, image=image_file)

            return Response(RouteSerializer(route, context={'request': request}).data, status=status.HTTP_201_CREATED)
        else:
          print("🔥 serializer.errors =>", serializer.errors) 
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])   
def comments_list_create(request, pk):
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = Comment.objects.filter(route=route).order_by('-created_at')
        data = [{
            "id": comment.id,
            "user_id": comment.user.id,
            "username": comment.user.username,
            "profile_picture": request.build_absolute_uri(comment.user.profile_picture.url) if comment.user.profile_picture else None,
            "text": comment.text,
            "created_at": comment.created_at
        } for comment in comments]
        return Response(data)

    elif request.method == 'POST':
        text = request.data.get('text')
        if not text:
            return Response({"error": "Comment text is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        Comment.objects.create(user=request.user, route=route, text=text)
        return Response({"message": "Comment added"}, status=status.HTTP_201_CREATED)

def comment_list_create(request, route_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(route_id=route_id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, route_id=route_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def route_detail(request, pk):
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH', 'DELETE']:
     if route.user != request.user:
        return Response({"error": "You do not have permission to modify this route."},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Kaydı güncelle
        if request.user.is_authenticated:
            ViewedRoute.objects.update_or_create(
                user=request.user, route=route
            )
        serializer = RouteSerializer(route, context={'request': request})
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = RouteSerializer(route, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            # Koordinatları güncelle
            RouteCoordinate.objects.filter(route=route).delete()
            coordinates_json = request.data.get('coordinates', '[]')
            try:
                coordinates = json.loads(coordinates_json)
            except json.JSONDecodeError:
                coordinates = []

            for coord in coordinates:
                RouteCoordinate.objects.create(
                    route=route,
                    latitude=coord.get("latitude"),
                    longitude=coord.get("longitude")
                )

            # Silinmesi istenen resimleri kaldır
            deleted_ids_raw = request.data.get("deleted_image_ids", "[]")
            try:
                deleted_ids = json.loads(deleted_ids_raw)
                if isinstance(deleted_ids, list):
                    RouteImage.objects.filter(route=route, id__in=deleted_ids).delete()
            except json.JSONDecodeError:
                pass

            # Yeni eklenen fotoğrafları kaydet
            for image_file in request.FILES.getlist('images'):
                RouteImage.objects.create(route=route, image=image_file)

            return Response(RouteSerializer(route, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        route.is_deleted = True
        route.deleted_at = timezone.now()
        route.save()
        return Response({"message": "Route marked as deleted."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def public_route_list(request):
    query = request.query_params.get('q', '').strip()

    # 🔥 Kullanıcı arama yaptıysa logla
    if query:
        log_search_term(request.user, query)

    routes = Route.objects.select_related("user").prefetch_related("images", "coordinates").filter(is_deleted=False)

    # 🔍 Sorgu varsa filtrele
    if query:
        routes = routes.filter(title__icontains=query)

    routes = routes.order_by('-created_at')
    serializer = RouteSerializer(routes, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_liked(request, pk):
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    liked = Like.objects.filter(user=request.user, route=route).exists()
    return Response({
        "is_liked": liked,
        "likes_count": route.likes.count()
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])  # Herkes erişebilir
def popular_routes(request):
    routes = (
        Route.objects
        .filter(is_deleted=False)
        .annotate(likes_count=Count('likes'))
        .order_by('-likes_count')[:6]  # en çok beğenilen ilk 10
        .select_related('user')
        .prefetch_related('images', 'coordinates')
    )
    serializer = RouteSerializer(routes, many=True, context={'request': request})
    return Response(serializer.data)

from django.db.models import Case, When, IntegerField, Value, F, Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suggested_routes(request):
    user = request.user
    liked_ids = Like.objects.filter(user=user).values_list('route_id', flat=True)

    # Başlangıç queryset'i
    base_qs = Route.objects.filter(is_deleted=False).exclude(id__in=liked_ids)

    # Skor işlemi için Q objeleri
    top_terms = get_top_search_terms(user)
    viewed_titles = get_viewed_titles(user)

    score_cases = []

    # 🔍 Arama geçmişi için +10 puan
    for term_data in top_terms:
        score_cases.append(
            When(title__icontains=term_data['term'], then=Value(10))
        )

    # 👁️ Ziyaret edilen başlıklar için +5 puan
    for title in viewed_titles:
        score_cases.append(
            When(title__icontains=title, then=Value(5))
        )

    # Skor anotasyonu
    base_qs = base_qs.annotate(
        score=Case(
            *score_cases,
            default=Value(0),
            output_field=IntegerField()
        )
    )

    base_qs = base_qs.annotate(likes_count=Count('likes')) \
                     .select_related('user') \
                     .prefetch_related('images', 'coordinates') \
                     .order_by('-score', '-likes_count')[:6]

    suggestions = list(base_qs)
    random.shuffle(suggestions)  # önerileri karıştır
    suggestions = suggestions[:6]  # ilk 6'sını al

    # Fallback rastgele öneri
    if not suggestions:
     suggestions = list(
        Route.objects
        .filter(is_deleted=False)
        .annotate(random_order=Random())
        .order_by('random_order')[:6]
        .select_related('user')
        .prefetch_related('images', 'coordinates')
    )

    serializer = RouteSerializer(suggestions, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, pk):
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    like, created = Like.objects.get_or_create(user=request.user, route=route)

    if not created:
        like.delete()
        return Response({"liked": False})
    else:
        return Response({"liked": True})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_search_view(request):
    term = request.data.get('term', '').strip()
    if not term:
        return Response({"error": "Term is required"}, status=400)

    SearchLog.objects.create(user=request.user, term=term.lower())
    return Response({"message": "Search term logged."}, status=201)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, route_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, route_id=route_id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Yetkilendirme: Yorumu yazan kullanıcı veya rota sahibi mi?
    if request.user == comment.user or request.user == comment.route.user:
        comment.delete()
        return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "You do not have permission to delete this comment."},
                        status=status.HTTP_403_FORBIDDEN)