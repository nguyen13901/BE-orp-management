from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_children.models import Children
from api_children.serializers import ChildrenSerializer
from api_children.services import ChildrenService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType, HttpMethod


class ChildrenViewSet(BaseViewSet):
    view_set_name = "children"
    queryset = Children.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = ChildrenSerializer
    required_alternate_scopes = {
        "list": [],
        "retrieve": [],
        "update": ["children:edit_children_info"],
        "create": ["children:edit_children_info"],
        "destroy": ["children:edit_children_info"],
        "destroy_multi": ["children:edit_children_info"],
        "remove_photo": ["children:edit_children_info"],
    }

    def list(self, request, *args, **kwargs):
        queryset = ChildrenService.get_filter_query(request)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=ChildrenService.init_data_children(request))
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["children"])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=ChildrenService.upload_image_data_children(request))
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                self.perform_update(serializer)
                if getattr(instance, "_prefetched_objects_cache", None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_200_OK)
        return ErrorResponse(ErrorResponseType.CANT_UPDATE, params=["children"])

    @action(methods=[HttpMethod.DELETE], detail=True)
    def remove_photo(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.personal_picture = None
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error_message": "Children id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HttpMethod.POST], detail=False)
    def destroy_multi(self, request, *args, **kwargs):
        children_ids = request.data.get("children_ids")
        if children_ids:
            is_deleted = ChildrenService.destroy_multi_children(children_ids)
            if is_deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return ErrorResponse(ErrorResponseType.CANT_DELETE, params=["children"])
