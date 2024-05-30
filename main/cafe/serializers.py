from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    image = serializers.ImageField(read_only=True)
    category = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.image = validated_data.get("image", instance.image)
        instance.v = validated_data.get("category", instance.category)
        instance.save()
        return  instance