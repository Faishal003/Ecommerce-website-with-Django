from django.contrib import admin
from django.urls import path, include

#To show media file
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App_Shop.urls')),
    path('accounts/', include('App_Login.urls')),
    path('shop/', include('App_Order.urls')),
    path('payment/', include('App_Payment.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
