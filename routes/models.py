from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()

class Route(models.Model):
    """Kullanıcıların oluşturduğu seyahat rotalarını temsil eder"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routes")
    title = models.CharField(max_length=255, default="Untitled", null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class RouteImage(models.Model):
    """Rotaya bağlı birden fazla fotoğrafı saklayan model"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='routes/images/')

    def __str__(self):
        return f"{self.route.title} - {self.image.url}"
    
class RouteCoordinate(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="coordinates")
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.route.title} ({self.latitude}, {self.longitude})"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    route = models.ForeignKey('Route', on_delete=models.CASCADE, related_name="likes")  # TIRNAK içinde 'Route'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'route')

    def __str__(self):
        return f"{self.user.username} liked {self.route.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    route = models.ForeignKey('Route', on_delete=models.CASCADE, related_name="comments")  # TIRNAK içinde 'Route'
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.route.title}"
    
class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_logs')
    term = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched: {self.term}"
    
class ViewedRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'route')