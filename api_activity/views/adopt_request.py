from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_activity.models import AdoptRequest
from api_activity.serializers import AdoptRequestSerializer
from api_activity.services import AdoptRequestService
from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.base import ErrorResponse, ErrorResponseType, HttpMethod


class AdoptRequestViewSet(BaseViewSet):
    view_set_name = "adopt_request"
    queryset = AdoptRequest.objects.all()
    permission_classes = [MyActionPermission]
    serializer_class = AdoptRequestSerializer
    required_alternate_scopes = {
        "retrieve": ["adopt_request:view_adopt_request"],
        "list": ["adopt_request:view_adopt_request"],
        "create": ["adopt_request:create_adopt_request"],
        "update": ["adopt_request:update_adopt_request"],
    }

    def create(self, request, *args, **kwargs):
        serializer = AdoptRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                serializer.save()
                AdoptRequestService.send_notify(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorResponse(ErrorResponseType.CANT_CREATE, params=["adopt_request"])

    @action(methods=[HttpMethod.PUT], detail=True)
    def do_action(self, request, *args, **kwargs):
        instance = self.get_object()
        action_request = request.query_params.get("action")
        # if instance and AdoptRequestService.check_action_request(instance, action_request):
        if instance:
            approver = request.user.profile
            res_data = self.get_serializer(AdoptRequestService.do_action(instance, approver, action_request)).data
            return Response(res_data, status=status.HTTP_200_OK)
        return ErrorResponse(ErrorResponseType.CANT_UPDATE, params=["adopt_request"])
