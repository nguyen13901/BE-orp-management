from rest_framework.decorators import action
from rest_framework.response import Response

from base.permission.permission import MyActionPermission
from base.views import BaseViewSet
from common.constants.api_user.scope_group import Scope
from common.constants.base import HttpMethod
from core.settings import SCOPES


class AuthViewSet(BaseViewSet):
    view_set_name = "account"
    permission_classes = [MyActionPermission]
    required_alternate_scopes = {
        "retrieve_all_scopes": ["role:edit"],
    }

    @action(methods=[HttpMethod.GET], detail=False)
    def retrieve_all_scopes(self, request, *args, **kwargs):
        scope_dict = SCOPES
        result = []
        for key in scope_dict.keys():
            resource = Scope.GROUP_SCOPE.get(key.split(":")[0].strip())
            result.append({"scope": key, "label": scope_dict.get(key), "group": resource})
        return Response({"scope": result})
