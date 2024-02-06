from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('employer/', include('employer.urls'), name='home-employer'),
    path('employee/', include('employee.urls'), name='home-employee'),
    path('story/', include('story.urls'), name='home-story'),

    path('', include('employee.urls'), name='home'),

    path('users/', include('users.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
