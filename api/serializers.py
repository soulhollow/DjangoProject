# api/serializers.py
from rest_framework import serializers
from contacts.models import Contact, Policy
from pipelines.models import Pipeline, Stage, PipelineContact
from teams.models import TeamMember
from core.models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_premium']
        read_only_fields = ['is_premium']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ContactSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['user', 'lead_score']


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'
        read_only_fields = ['contact']


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'
        read_only_fields = ['user']


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'
        read_only_fields = ['pipeline']


class PipelineContactSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    stage = StageSerializer(read_only=True)

    class Meta:
        model = PipelineContact
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']


class TeamMemberSerializer(serializers.ModelSerializer):
    downline = UserSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'downline', 'level']