# api/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from core.models import User, Task, Tag
from contacts.models import Contact, Policy
from pipelines.models import Pipeline, Stage, PipelineContact
from teams.models import TeamMember


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def policies(self, request, pk=None):
        contact = self.get_object()
        policies = Policy.objects.filter(contact=contact)
        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        contact = self.get_object()
        tasks = Task.objects.filter(contact=contact)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        from datetime import datetime, timedelta
        now = datetime.now()
        one_week_later = now + timedelta(days=7)
        tasks = Task.objects.filter(
            user=request.user,
            completed=False,
            due_date__range=(now, one_week_later)
        ).order_by('due_date')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class PipelineViewSet(viewsets.ModelViewSet):
    serializer_class = PipelineSerializer

    def get_queryset(self):
        return Pipeline.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def stages(self, request, pk=None):
        pipeline = self.get_object()
        stages = Stage.objects.filter(pipeline=pipeline)
        serializer = StageSerializer(stages, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Nur für Premium-Nutzer
        if not self.request.user.is_premium:
            return TeamMember.objects.none()

        return TeamMember.objects.filter(
            upline=self.request.user,
            level=1  # Nur direkte Partner (1. Linie)
        )