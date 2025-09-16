from rest_framework import serializers
from .models import Solution , Step

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'

class SolutionCreateSerializer(serializers.Serializer):
    question = serializers.CharField()
    steps = serializers.ListField(child=serializers.CharField())
