from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('module/', include('modules.urls',namespace='modules')),
    path('product/', include('products.urls',namespace='products'))
]