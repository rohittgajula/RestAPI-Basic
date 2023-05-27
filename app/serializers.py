from rest_framework import serializers
from .models import *

class loginSerializer(serializers.Serializer):
    email = serializers.EmailField()
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

