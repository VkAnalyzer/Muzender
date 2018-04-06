from django.conf.urls import url, include
from .views import VkProfileViewSet, index_page
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api', VkProfileViewSet)

urlpatterns = [
    url(r'^$', index_page, name='music'),
    url(r'', include(router.urls))
]
