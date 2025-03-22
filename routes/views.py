from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Route, RouteLocation, RouteImage, Comment, Like
from .serializers import RouteSerializer, RouteLocationSerializer, RouteImageSerializer, CommentSerializer, LikeSerializer

# Route List & Create
class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all().order_by('-created_at')
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Route Detail (Retrieve, Update, Delete)
class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

# Add Location to Route
class AddRouteLocationView(generics.CreateAPIView):
    serializer_class = RouteLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk, user=request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(route=route)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Upload Image to Route
class UploadRouteImageView(generics.CreateAPIView):
    serializer_class = RouteImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk, user=request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(route=route)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Comment on Route
class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        route_id = self.kwargs['pk']
        return Comment.objects.filter(route_id=route_id)

    def perform_create(self, serializer):
        route = get_object_or_404(Route, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, route=route)

# Like or Unlike a Route
class LikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, route=route)
        if created:
            return Response({"message": "Beğenildi!"}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({"message": "Beğeni kaldırıldı!"}, status=status.HTTP_200_OK)
