from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver

class Command(BaseCommand):
    help = "List all URL patterns and their names"

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        self.list_urls(url_patterns)

    def list_urls(self, patterns, prefix=""):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):  # Якщо це звичайний шлях
                self.stdout.write(f"Path: {prefix}{pattern.pattern}, Name: {pattern.name}")
            elif isinstance(pattern, URLResolver):  # Якщо це include()
                self.stdout.write(f"Included: {prefix}{pattern.pattern}")
                # Рекурсивно обробляємо вкладені шляхи
                self.list_urls(pattern.url_patterns, prefix=f"{prefix}{pattern.pattern}")