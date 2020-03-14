from rest_framework import serializers
from userForms.models import UserDetails,Notes
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class RegisterationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['username','email','password','confirm_password']

class LoginFormFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['username','password']

class ForgotPasswordFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['email']

class ResetPasswordFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['password','confirm_password']

class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title','takeNote','archive','pin','bin']
        # read_only_fileds = ['user']

class DisplayNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fileds = ['user']

class RestoreNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['bin']