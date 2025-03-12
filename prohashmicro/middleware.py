import importlib
from django.conf import settings
from django.urls import resolve, Resolver404
from django.http import HttpResponseForbidden
from modules.models import Module

class BlockUninstalledModulesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.urls_master = []
        self.urls_blocked = []

        # Inisialisasi URL yang diblokir
        self.initialize_blocked_urls()

    def initialize_blocked_urls(self):
        # Import URL patterns dari prohashmicro
        from prohashmicro import urls as phurls

        # Tambahkan semua URL patterns dari prohashmicro ke urls_master
        for u in phurls.urlpatterns:
            if hasattr(u, 'url_patterns'):  # Periksa apakah ini include()
                for up in u.url_patterns:
                    if up not in self.urls_master:
                        self.urls_master.append(up)
            else:  # Jika ini adalah URLPattern biasa
                if u not in self.urls_master:
                    self.urls_master.append(u)

        # Cari modul dengan status 'Uninstalled' dan blokir URL-nya
        for m in Module.objects.filter(status='Uninstalled'):
            try:
                urls = importlib.import_module(f"{m.name}.urls")
                for u in urls.urlpatterns:
                    if hasattr(u, 'url_patterns'):  # Periksa apakah ini include()
                        for up in u.url_patterns:
                            if up not in self.urls_blocked:
                                self.urls_blocked.append(up)
                    else:  # Jika ini adalah URLPattern biasa
                        if u not in self.urls_blocked:
                            self.urls_blocked.append(u)
            except ImportError:
                # Jika modul tidak ditemukan, lewati
                continue

    def __call__(self, request):
        # Resolve URL yang diminta
        try:
            resolved_url = resolve(request.path_info)
        except Resolver404:
            # Jika URL tidak ditemukan, lanjutkan ke middleware berikutnya
            return self.get_response(request)

        # Periksa apakah URL yang diminta diblokir
        for blocked_url in self.urls_blocked:
            # Bandingkan nama URL (name) dari resolved_url dengan blocked_url
            if resolved_url.url_name == getattr(blocked_url, 'name', None):
                # Jika URL diblokir, kembalikan respons 403 Forbidden
                return HttpResponseForbidden("Access to this URL is blocked.")

        # Lanjutkan ke middleware berikutnya atau view
        return self.get_response(request)