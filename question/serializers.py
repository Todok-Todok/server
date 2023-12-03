from .models import Question,UserQuestion
from rest_framework import serializers, validators

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        

class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = '__all__'
        

class QuestionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('content','disclosure',)
        

class QuestionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_id','content',)
        


class UserQuestionReactionSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    
    def get_avatar_url(self, obj):
        return obj.user.avatar_url
    
    class Meta:
        model = UserQuestion
        fields = ('id','opinion','like','avatar_url',)
        