from collections import OrderedDict

from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response


class CommonModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'retrieve_serializer_class'):
                return self.retrieve_serializer_class
        elif self.action == 'partial_update':
            if hasattr(self, 'update_serializer_class'):
                return self.update_serializer_class
        elif self.action == 'create':
            if hasattr(self, 'create_serializer_class'):
                return self.create_serializer_class
        elif self.action == 'list':
            if hasattr(self, 'list_serializer_class'):
                return self.list_serializer_class

        return super().get_serializer_class()



