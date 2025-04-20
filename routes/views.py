from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from routes.models import Route, RouteCoordinate, RouteImage
from routes.serializers import RouteSerializer, RouteImageSerializer
import json
from django.utils import timezone


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def route_list(request):
    if request.method == 'GET':
        # 🔥 Sadece giriş yapan kullanıcıya ait rotaları döndür
        routes = Route.objects.filter(user=request.user)
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            route = serializer.save(user=request.user)

            # 🔁 Koordinatları kaydet
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

            # 🖼 Fotoğrafları kaydet
            for image_file in request.FILES.getlist('images'):
                RouteImage.objects.create(
                    route=route,
                    image=image_file
                )

            return Response(RouteSerializer(route).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def route_detail(request, pk):
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    # ❗️ Sadece rotayı oluşturan kullanıcı işlem yapabilir
    if route.user != request.user:
        return Response({"error": "You do not have permission to modify this route."},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = RouteSerializer(route)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RouteSerializer(route, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
     route.is_deleted = True
    route.deleted_at = timezone.now()  # 🆕 zamanı kaydet
    route.save()
    return Response({"message": "Route marked as deleted."}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([])
def public_route_list(request):
    """
    Tüm kullanıcıların rotalarını döndürür. (Search sayfası için)
    """
    routes = Route.objects.select_related("user").prefetch_related("images", "coordinates").order_by('-created_at')
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)