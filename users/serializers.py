from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group
User = get_user_model()



class UserCreateSerializer(BaseUserCreateSerializer):
    prof_image = serializers.ImageField(required=False)
    phone_number=serializers.CharField(required=False)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name',
                  'last_name', 'address', 'phone_number','prof_image']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        #(Directy add to clients group)
        client_group, created = Group.objects.get_or_create(name='Clients')
        user.groups.add(client_group)
        return user


class UserSerializer(BaseUserSerializer):
    prof_image=serializers.ImageField()
    class Meta(BaseUserSerializer.Meta):
        ref_name='CustomUser'
        fields = ['id', 'email', 'first_name',
                  'last_name', 'address', 'phone_number','prof_image']
        


class PromoteUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','first_name','email','is_staff']
        read_only_fields=['first_name','email']

    def validate_is_staff(self, value):
        # Only allow promotion by admin
        request = self.context.get('request')
        if not request or not request.user.is_staff:
            raise serializers.ValidationError("Only admins can change staff status.")
        return value