from rest_framework import serializers
from . models import Audio_store,Skill
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','email',
                  'zip_code','phone','state','city','score']
        
class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio_store
        fields = ['record']
        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['package','amount']