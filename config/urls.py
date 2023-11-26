from django.urls import path, include


urlpatterns = [
    # path("api/vi/", include(router.urls)),
    # path("ht/", include("health_check.urls")),
    path("v1/system/", include("core.urls", namespace="system")),
]
