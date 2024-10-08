from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q

from bases.models import Status
from requests.models import Request
from requests.serializers import RequestSerializer


class RequestByPViewSet(ListModelMixin, GenericViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(self):
        p_id = self.kwargs['project_id']
        u_id = self.kwargs['user_id']
        exclude_list = Status.objects.filter(status_en__in=['Done', 'Cancel'])
        queryset = Request.objects.filter(project=p_id, belong_to=None)\
            .exclude(status__in=exclude_list).order_by('-status', 'level', 'due_date')

        return queryset


class SubRequestViewSet(ListModelMixin, GenericViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(self):
        r_id = self.kwargs['request_id']
        queryset = Request.objects.filter(belong_to=r_id).order_by('due_date')

        return queryset

