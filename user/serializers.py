from .models import User
from rest_framework import serializers, validators

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
                "password": {"write_only":True},
                "username": {
                    "required": True,
                    "allow_blank": False,
                    "validators":[
                        validators.UniqueValidator(
                            User.objects.all(), "A user with that Email already exists"
                        )
                    ]
                }
            }
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            nickname= validated_data['nickname']
        )
        return user
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    