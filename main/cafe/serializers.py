from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('name', 'description', 'image', 'category')
    

    # def create(self, validated_data):
    #     return Menu.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.description = validated_data.get("description", instance.description)
    #     instance.image = validated_data.get("image", instance.image)
    #     instance.v = validated_data.get("category", instance.category)
    #     instance.save()
    #     return  instance