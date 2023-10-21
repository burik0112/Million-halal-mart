from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .scheme import swagger_urlpatterns

urlpatterns = [
    path("api/customer/", include("apps.customer.urls")),
    path("api/product/", include("apps.product.urls")),
    path("api/merchant/", include("apps.merchant.urls")),
    path("admin/", admin.site.urls, name="admin"),
] + swagger_urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
