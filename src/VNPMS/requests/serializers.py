from rest_framework import serializers

from bases.serializers import StatusSerializer
from problems.models import Problem
from requests.models import Request, Level
from users.serializers import UserSerializer


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    sub_request = serializers.SerializerMethodField()
    nested = serializers.SerializerMethodField()
    status = StatusSerializer(many=False, read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Request
        fields = '__all__'


    def get_nested(self, obj):
        sub_requests = Request.objects.filter(belong_to=obj)
        return sub_requests.count()

    def get_sub_request(self, obj):
        sub_num = '-'
        f_num = 0
        sub_requests = Request.objects.filter(belong_to=obj).order_by('due_date')

        if sub_requests.count() > 0:
            for sub_request in sub_requests:
                if sub_request.process_rate == 100:
                    f_num += 1
            sub_num = '{sub_request}/{total_request}'.format(sub_request=str(f_num),
                                                             total_request=str(sub_requests.count()))
        return sub_num

    def get_problem_num(self, obj):
        problem_num = Problem.objects.all().count()

        return problem_num


# class RequestByPSerializer(serializers.ModelSerializer):
#     sub_request = serializers.SerializerMethodField()
#     problem_num = serializers.SerializerMethodField()
#     nested = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Request
#         fields = '__all__'
#
#     def get_nested(self, obj):
#         sub_requests = Request.objects.filter(belong_to=obj)
#         return sub_requests.count()
#
#
#     def get_sub_request(self, obj):
#         sub_num = '-'
#         f_num = 0
#         sub_requests = Request.objects.filter(belong_to=obj)
#
#         if sub_requests.count() > 0:
#             for sub_request in sub_requests:
#                 if sub_request.process_rate == 100:
#                     f_num += 1
#             sub_num = '{sub_request}/{total_request}'.format(sub_request=str(f_num),
#                                                              total_request=str(sub_requests.count()))
#         return sub_num
#
#
#     def get_problem_num(self, obj):
#         problem_num = Problem.objects.filter(belong_to=obj.request_no).count()
#
#         return problem_num