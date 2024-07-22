from rest_framework import serializers
from problems.models import Problem_reply, Problem
from users.serializers import UserSerializer


class ProblemSerializer(serializers.ModelSerializer):
    reply_num = serializers.SerializerMethodField()
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    create_by = UserSerializer(many=False, read_only=True)
    update_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'

    def get_reply_num(self, obj):
        reply_num = Problem_reply.objects.filter(problem_no=obj)
        return reply_num.count()