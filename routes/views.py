from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Route, RouteImage
from .serializers import RouteSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Kullanıcının giriş yapması zorunlu
def route_create(request):
    user = request.user
    title = request.data.get('title')
    description = request.data.get('description')
    images = request.FILES.getlist('images')  # Birden fazla dosya al

    route = Route.objects.create(user=user, title=title, description=description)

    for image in images:
        RouteImage.objects.create(route=route, image=image)  # Her görseli ayrı kaydet

    serializer = RouteSerializer(route)
    return Response(serializer.data, status=201)
