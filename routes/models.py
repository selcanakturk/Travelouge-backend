from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Route(models.Model):
    """Kullanıcıların oluşturduğu seyahat rotalarını temsil eder"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routes")
    title = models.CharField(max_length=255, default="Untitled", unique=True,null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class RouteImage(models.Model):
    """Rotaya bağlı birden fazla fotoğrafı saklayan model"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='routes/images/')

    def __str__(self):
        return f"{self.route.title} - {self.image.url}"
