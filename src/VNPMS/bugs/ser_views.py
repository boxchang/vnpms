from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from bugs.models import Bug
from bugs.serializers import BugSerializer


class BugByPViewSet(ListModelMixin, GenericViewSet):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer

    def get_queryset(self):
        p_id = self.kwargs['project_id']
        queryset = Bug.objects.filter(project=p_id)

        return queryset