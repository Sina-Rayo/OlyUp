from rest_framework import serializers
from .models import Account ,Recepie ,Categorie ,Comment ,Ingredient

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recepie
        fields = '__all__'

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class SolutionCreateSerializer(serializers.Serializer):
    question = serializers.CharField()
    steps = serializers.ListField(child=serializers.CharField())
