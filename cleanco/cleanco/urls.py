from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls")),  # store app
    path("cart/", include("cart.urls")),  # cart app
    path("account/", include("account.urls")),  # acount app
    path("payment/", include("payment.urls")),  # payment app
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
