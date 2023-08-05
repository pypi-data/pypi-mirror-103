from django.conf import settings

from rest_framework import routers

from .apis import ThreadViewSet, PostViewSet, TopicsViewSet


router = routers.DefaultRouter()
router.register(r'threads', ThreadViewSet, basename='threads')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'topics', TopicsViewSet, basename='topics')

if getattr(settings, 'REACT_COMMENTS_DJANGO_USE_INTERNAL_USER', None):
    from .apis import UserViewSet
    router.register(r'users', UserViewSet, basename='users')

# todo import users api if embed

urlpatterns = router.urls

