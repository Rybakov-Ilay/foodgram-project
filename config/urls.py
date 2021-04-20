from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.conf.urls import handler404, handler500, handler400

handler400 = 'config.views.page_bad_request'  # noqa
handler404 = 'config.views.page_not_found'  # noqa
handler500 = 'config.views.server_error'  # noqa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about-us/", views.flatpage, {"url": "/about-us/"}, name="about"),
    path("tech/", views.flatpage, {"url": "/tech/"}, name="tech"),
    path("api/", include("api.urls")),
    path("", include("recipes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
