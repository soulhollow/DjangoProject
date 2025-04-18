# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, TaskViewSet, PipelineViewSet, TeamViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'pipelines', PipelineViewSet, basename='pipeline')
router.register(r'team', TeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
]