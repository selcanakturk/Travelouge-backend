from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from routes.models import Route, RouteCoordinate, RouteImage
from routes.serializers import RouteSerializer, RouteImageSerializer
import json


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
@api_view(['GET', 'POST'])
def route_detail(request, pk):
    """Belirli bir rotayı detaylı göster veya ona resim ekle"""
    try:
        route = Route.objects.get(pk=pk)
    except Route.DoesNotExist:
        return Response({"error": "Route not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RouteSerializer(route)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Rota ile ilişkilendirilen bir resim ekle
        serializer = RouteImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(route=route)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([])  # Giriş yapmadan da erişilebilir istersen AllowAny da yazabilirsin
def public_route_list(request):
    """
    Tüm kullanıcıların rotalarını döndürür. (Search sayfası için)
    """
    routes = Route.objects.all().order_by('-created_at')  # isteğe göre sıralanabilir
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)