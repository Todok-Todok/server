from rest_framework import serializers, validators
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','password')
        
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
        user = User(
            username=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user