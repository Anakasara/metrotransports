from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vnineapp.urls')),
    path('', RedirectView.as_view(url='/api/', permanent=False)),  # Redirect root URL to /api/
]
