from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('jet/', include('jet.urls','jet')),
    path('jet/dashboard/', include('jet.dashboard.urls','jet-dashboard')),
    # path('', include('admin_material.urls')),
    path('admin/', admin.site.urls),
    # path('admin_tools_stats',include('admin_tools_stats.urls')),
    path('',include('main.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
]

