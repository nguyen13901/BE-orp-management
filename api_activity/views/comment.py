from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api_activity.models import Comment
from api_activity.serializers import CommentSerializer, CommentDetailSerializer
from api_activity.services import CommentService
from api_user.utils.scopes import is_valid_auth
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType


class CommentViewSet(BaseViewSet):
    view_set_name = "comment"
    queryset = Comment.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = CommentSerializer
    serializer_map = {
        "list": CommentDetailSerializer
    }
    pagination_class = None
    required_alternate_scopes = {
        "list": [],
        "create": ['activity:comment_activity'],
        "destroy": ['activity:delete_all_comment']
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        data['parent'] = None if data['parent'] == "" or data['parent'] == "undefined" else data['parent']
        data['account'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["comment"])

    def list(self, request, *args, **kwargs):
        queryset = CommentService.get_filter_query(request)
        serializers = self.get_serializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if is_valid_auth('activity:delete_all_comment', request.user) or request.user.id == instance.account.id:
            with transaction.atomic():
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return ErrorResponse(ErrorResponseType.CANT_DELETE, params=["comment"])
