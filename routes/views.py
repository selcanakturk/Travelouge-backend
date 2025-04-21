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
        routes = Route.objects.filter(user=request.user)
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RouteSerializer(data=request.data)
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
                RouteImage.objects.create(
                    route=route,
                    image=image_file
                )

            return Response(RouteSerializer(route).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def route_detail(request, pk):
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    if route.user != request.user:
        return Response({"error": "You do not have permission to modify this route."},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = RouteSerializer(route)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = RouteSerializer(route, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # 🔁 Koordinatları güncelle
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

            # 🧹 Silinmesi istenen resimleri kaldır
            deleted_ids_raw = request.data.get("deleted_image_ids", "[]")
            try:
                deleted_ids = json.loads(deleted_ids_raw)
                if isinstance(deleted_ids, list):
                    RouteImage.objects.filter(route=route, id__in=deleted_ids).delete()
            except json.JSONDecodeError:
                pass

            # 🆕 Yeni eklenen fotoğrafları kaydet
            for image_file in request.FILES.getlist('images'):
                RouteImage.objects.create(route=route, image=image_file)

            return Response(RouteSerializer(route).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        route.is_deleted = True
        route.deleted_at = timezone.now()
        route.save()
        return Response({"message": "Route marked as deleted."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
def public_route_list(request):
    routes = Route.objects.select_related("user").prefetch_related("images", "coordinates").order_by('-created_at')
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)