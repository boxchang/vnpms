from rest_framework import serializers
from borrow.models import Borrow, BorrowItem
from users.serializers import UserSerializer


class BorrowSerializer(serializers.ModelSerializer):
    lend_owner = UserSerializer(many=False, read_only=True)
    return_owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Borrow
        fields = '__all__'


class BorrowItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowItem
        fields = '__all__'
