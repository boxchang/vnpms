from rest_framework import serializers
from problems.models import Problem_reply, Problem, ProblemType
from users.serializers import UserSerializer


class ProblemSerializer(serializers.ModelSerializer):
    reply_num = serializers.SerializerMethodField()
    problem_type_name = serializers.SerializerMethodField()
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    create_by = UserSerializer(many=False, read_only=True)
    update_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'

    def get_problem_type_name(self, obj):
        return obj.problem_type.type_name if obj.problem_type else None

    def get_reply_num(self, obj):
        reply_num = Problem_reply.objects.filter(problem_no=obj)
        return reply_num.count()