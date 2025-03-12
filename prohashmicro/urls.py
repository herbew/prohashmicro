from django.urls import include, path
from django.contrib import admin

from products.views import ProductListView

urlpatterns = [
	path('',ProductListView.as_view()),
    path('admin/', admin.site.urls),
    path('module/', include('modules.urls',namespace='modules')),
    path('product/', include('products.urls',namespace='products'))
]