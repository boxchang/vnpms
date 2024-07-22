from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from bugs.models import Bug
from problems.models import Problem
from problems.serializers import ProblemSerializer


class ProblemByPViewSet(ListModelMixin, GenericViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        p_pk = self.kwargs['project_id']
        exclude_list = [6, 8]
        queryset = Problem.objects.filter(project=p_pk).exclude(problem_status__in=exclude_list)

        return queryset


class ProblemByRViewSet(ListModelMixin, GenericViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        r_pk = self.kwargs['request_id']
        queryset = Problem.objects.filter(belong_to=r_pk)

        return queryset


class ProblemByBViewSet(ListModelMixin, GenericViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        b_pk = self.kwargs['bug_id']
        queryset = Problem.objects.filter(belong_to=b_pk)

        return queryset