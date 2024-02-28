from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .scheme import swagger_urlpatterns
from django.shortcuts import redirect
from apps.dashboard.users import user_login, user_logout
import debug_toolbar
def redirect_dashboard(request):
    return redirect("dashboard")


urlpatterns = [
    path("api/customer/", include("apps.customer.urls")),
    path("api/product/", include("apps.product.urls")),
    path("api/merchant/", include("apps.merchant.urls")),
    path("admin/", admin.site.urls, name="admin"),
    path(
        "dashboard/", include("apps.dashboard.urls"), name="dashboard"
    ),
    path("__debug__/", include(debug_toolbar.urls)),
    path("login/", user_login, name="login_page"),
    path('logout/', user_logout, name='logout'),
    path("", redirect_dashboard),
] + swagger_urlpatterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
