from rest_framework import serializers

from bases.serializers import StatusSerializer
from bugs.models import Bug
from requests.serializers import LevelSerializer
from users.serializers import UserSerializer


class BugSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    status = StatusSerializer(many=False, read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    owner = UserSerializer(many=False, read_only=True)
    create_by = UserSerializer(many=False, read_only=True)


    class Meta:
        model = Bug
        fields = '__all__'