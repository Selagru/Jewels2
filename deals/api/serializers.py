from rest_framework import serializers
from deals.models import Deal
from items.models import Item
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name']


class TopFiveSerializer(serializers.ModelSerializer):
    total_spent = serializers.IntegerField(read_only=True, required=False)
    gems = ItemSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'total_spent', 'gems']


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'


class UploadSerializer(serializers.Serializer):
    deals = serializers.FileField()

    def create(self, validated_data):
        return None
