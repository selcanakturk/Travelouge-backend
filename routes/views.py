from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from routes.models import Route, RouteImage
from routes.serializers import RouteSerializer, RouteImageSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def route_list(request):
    """Rotaları listele veya yeni rota ekle"""
    if request.method == 'GET':
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            # Yeni rotayı kaydet
            route = serializer.save(user=request.user)  # kullanıcıyı almak için request.user kullan
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
