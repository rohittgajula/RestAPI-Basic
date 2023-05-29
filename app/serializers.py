from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User

# ---- For registration 

class RegisterSerilizer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):               # to check if username already exists.
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username already exists.')
            
        if data['email']:                   # to check email already exists.
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('email already exists.')
        return data
    
    # def save(self):             # this method is used when you dont want to override .save() method in views
    #     username = self.validated_data['username']
    #     email = self.validated_data['email']
    #     password = self.validated_data['password']
    #     print({'username':username, 'email':email, 'password':password})

                        # | below method is used when save method is used in views

                        # as we are using serializers.Serializer, it doesnot contain built-in create, update method built-in umlike serializers.ModelSerializer
    
    def create(self, validated_data):       # to create user.
            user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
            user.set_password(validated_data['password'])
            user.save()
            return validated_data
            # print(validated_data)

class loginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# class ColorSerializer(serializers.ModelSerializer): # to get data from inner model
#     class Meta:
#         model = Color
#         fields = ['color_name', 'id']

class PersonSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    # color_info = serializers.SerializerMethodField()    # <---

    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1                   # gets all data from forigen key model. Hera gets data from color mmodel also.

    # def get_color_info(self, obj):      # more info about inner model.
    #     color_obj = Color.objects.get(id = obj.color.id)

    #     return {'color_name':color_obj.color_name, 'hex_code':'#000'}

    # def validate(self, data):             # cause error is 

    #     special_characters = "!@#$%^&*()_+:';<>,./`-"
    #     if any(c in special_characters for c in data['name']):
    #         raise serializers.ValidationError('name cannot contain special characters.')

    #     if data['age'] < 18: 
    #         raise serializers.ValidationError("age should be greated than 18")
    #     return data

