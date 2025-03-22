from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Location(models.Model):
    """Harita üzerinde bir konumu temsil eder"""
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def _str_(self):
        return self.name

class Route(models.Model):
    """Kullanıcıların oluşturduğu seyahat rotalarını temsil eder"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routes")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    locations = models.ManyToManyField(Location, related_name="routes")

    def _str_(self):
        return self.title

class RouteLocation(models.Model):
    """Rotada ziyaret edilen konumları ve sıralarını tutar"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_locations")
    latitude = models.FloatField()
    longitude = models.FloatField()
    order = models.IntegerField(default=0)  # Konumun rotadaki sırası

    class Meta:
        ordering = ['order']  # Varsayılan sıralama

    def _str_(self):
        return f"{self.route.title} - Sıra: {self.order}"

class RouteImage(models.Model):
    """Rotaya eklenen fotoğrafları tutar"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='routes/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.route.title} - Fotoğraf"

class Comment(models.Model):
    """Rotalara yapılan yorumları tutar"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.route.title} Yorumu"

class Like(models.Model):
    """Rotaya yapılan beğenileri tutar"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('route', 'user')  # Aynı kullanıcı bir rotayı sadece 1 kez beğenebilir

    def _str_(self):
        return f"{self.user.username} likes {self.route.title}"