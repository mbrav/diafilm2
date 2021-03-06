"""diafilm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.posts.urls', 'posts'), namespace=None)),
    path('api/', include(('apps.api.urls', 'api'), namespace='api')),
    path('about/', include(('apps.about.urls', 'about'), namespace='about')),
    path('auth/', include(('apps.user.urls', 'users'), namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),

    # django-debug-toolbar
    path('__debug__/', include(debug_toolbar.urls)),
]

handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'
handler403 = 'apps.core.views.permission_denied'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
