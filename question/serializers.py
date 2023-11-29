from .models import Question
from rest_framework import serializers, validators

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        

class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'