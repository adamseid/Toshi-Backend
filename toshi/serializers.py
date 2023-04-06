from rest_framework import serializers
from .models import test

class testSerializer(serializers.ModelSerializer):

    class Meta:
        model = test 
        fields = ('pk', 'name', 'email', 'document', 'phone', 'registrationDate')