from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


# Instead of router.register, use direct URL patterns
urlpatterns = [
    path("auth/", include("hirethon_template.users.api.urls")),
]

# If you want to keep the router for other apps, you can add them here
# router.register("some-other-model", SomeOtherViewSet)
# urlpatterns += router.urls
