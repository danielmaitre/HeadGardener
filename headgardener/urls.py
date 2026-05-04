from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", RedirectView.as_view(url="/plants/", permanent=False)),
    path("", include("garden.urls")),
] + static(settings.MEDIA_URL, document_root=getattr(settings, 'MEDIA_ROOT', ''))
