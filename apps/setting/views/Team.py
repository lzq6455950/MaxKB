# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： Team.py
    @date：2023/9/25 17:13
    @desc:
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.views import Request

from common.auth import TokenAuth
from common.response import result
from setting.serializers.team_serializers import TeamMemberSerializer, get_response_body_api, \
    UpdateTeamMemberPermissionSerializer


class TeamMember(APIView):
    authentication_classes = [TokenAuth]

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(operation_summary="获取团队成员列表",
                         operation_id="获取团员成员列表",
                         responses=result.get_api_response(get_response_body_api()))
    def get(self, request: Request):
        return result.success(TeamMemberSerializer(data={'team_id': str(request.user.id)}).list_member())

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(operation_summary="添加成员",
                         operation_id="添加成员",
                         request_body=TeamMemberSerializer().get_request_body_api())
    def post(self, request: Request):
        team = TeamMemberSerializer(data={'team_id': str(request.user.id)})
        return result.success((team.add_member(**request.data)))

    class Operate(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary="获取团队成员权限",
                             operation_id="获取团队成员权限",
                             manual_parameters=TeamMemberSerializer.Operate.get_request_params_api())
        def get(self, request: Request, member_id: str):
            return result.success(TeamMemberSerializer.Operate(
                data={'member_id': member_id, 'team_id': str(request.user.id)}).list_member_permission())

        @action(methods=['PUT'], detail=False)
        @swagger_auto_schema(operation_summary="修改团队成员权限",
                             operation_id="修改团队成员权限",
                             request_body=UpdateTeamMemberPermissionSerializer().get_request_body_api(),
                             manual_parameters=TeamMemberSerializer.Operate.get_request_params_api()
                             )
        def put(self, request: Request, member_id: str):
            return result.success(TeamMemberSerializer.Operate(
                data={'member_id': member_id, 'team_id': str(request.user.id)}).edit(request.data))

        @action(methods=['DELETE'], detail=False)
        @swagger_auto_schema(operation_summary="移除成员",
                             operation_id="移除成员",
                             manual_parameters=TeamMemberSerializer.Operate.get_request_params_api()
                             )
        def delete(self, request: Request, member_id: str):
            return result.success(TeamMemberSerializer.Operate(
                data={'member_id': member_id, 'team_id': str(request.user.id)}).delete())