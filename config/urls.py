from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path("api/vi/", include(router.urls)),
    # path("ht/", include("health_check.urls")),
    path("api/v1/", include("core.urls")),
    path("admin/", admin.site.urls),
]
