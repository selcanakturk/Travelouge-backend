from django.core.management.base import BaseCommand
from django.utils import timezone
from routes.models import Route
from datetime import timedelta

class Command(BaseCommand):
    help = "Soft silinen ve belirli süreyi aşan rotaları kalıcı olarak siler"

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timedelta(days=30)  # 🗓️ 30 gün geçmiş olanlar
        old_routes = Route.objects.filter(is_deleted=True, deleted_at__lt=threshold)

        count = old_routes.count()
        old_routes.delete()

        self.stdout.write(self.style.SUCCESS(f"{count} eski rota kalıcı olarak silindi."))