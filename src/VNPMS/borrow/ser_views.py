import json

from django.http import JsonResponse
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from borrow.models import Borrow, BorrowItem
from borrow.serializers import BorrowSerializer, BorrowItemSerializer
from rest_framework.response import Response


class BorrowByViewSet(ListModelMixin, GenericViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    def get_queryset(self):
        queryset = Borrow.objects.all().order_by('-update_at')
        return queryset




