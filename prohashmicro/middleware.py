import importlib
from django.urls import resolve, Resolver404
from django.http import HttpResponseForbidden
from modules.models import Module

class BlockUninstalledModulesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.urls_blocked = []

        # Blocked URL initialization
        self.initialize_blocked_urls()

    def initialize_blocked_urls(self):
        # Look for modules with 'uninstalled' status and block their URLs.
        for m in Module.objects.filter(status='uninstalled'):
            try:
                urls = importlib.import_module(f"{m.name}.urls")
                for u in urls.urlpatterns:
                    if hasattr(u, 'url_patterns'):  # Check if this is include()
                        for up in u.url_patterns:
                            if up not in self.urls_blocked:
                                self.urls_blocked.append(up)
                    else:  # If this is a regular URLPattern
                        if u not in self.urls_blocked:
                            self.urls_blocked.append(u)
            except ImportError:
                # if module not found, skip
                continue

    def __call__(self, request):
        """# Resolve the requested URL
        try:
            resolved_url = resolve(request.path_info)
        except Resolver404:
            # If URL is not found, proceed to the next middleware.
            return self.get_response(request)

        # Check if the requested URL is blocked
        for blocked_url in self.urls_blocked:
            # Compare the URL name of resolved_url with blocked_url
            if resolved_url.url_name == getattr(blocked_url, 'name', None):
                # If URL is blocked, return a 403 Forbidden response.
                return HttpResponseForbidden("Access to this URL is blocked.")
        """
        # Proceed to the next middleware or view
        return self.get_response(request)