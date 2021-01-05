from django.contrib.auth.backends import ModelBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from apps.user.models import UserProfile,Organ
from .seriailzers import RegisterSerializer,UserDetailSerializer,AdminSerializer,UpdateUserSerializer,PasswordSerializer,OrganSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
import operator
from utils.permissions import UserPermission,AdminPermission,TeacherPermission
from rest_framework import mixins
from rest_framework import viewsets

class P1(PageNumberPagination):
    """
    基于页码
    """
    # 默认每页显示的数据条数
    page_size = 10
    # 获取url参数中设置的每页显示数据条数
    page_size_query_param = 'pagesize'
    # 获取url中传入的页码key
    page_query_param = 'page'
    # 最大支持的每页显示的数据条数
    max_page_size = 50


class UserViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin):
    """
    用户操作
    post:创建用户
    put: 修改用户
    get: 查看登录用户详情
    """


    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # permission_classes = (IsAuthenticated,UserPermission)
    def get_permissions(self):
        if self.action == "create":
            return ()
        else:
            return (IsAuthenticated(),UserPermission())

    def create(self,request,*args,**kwargs):
        # 校验参数
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存
        serializer.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self,request,*args,**kwargs):


        serializer = UserDetailSerializer(instance=request.user,many=False)
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # 校验参数
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserProfile.objects.filter(id=request.user.id).update(**serializer.validated_data)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)



class AdminViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    """
       用户操作
       post:创建用户
       put: 通过用户
       list:查看用户
    """
    serializer_class = AdminSerializer
    pagination_class = P1
    queryset = UserProfile.objects.filter(role=0).all().order_by("logintime")

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,AdminPermission)

    def create(self, request, *args, **kwargs):

        # 校验参数
        serializer = AdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存
        serializer.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = request.data.get("id",0)
        check = request.data.get("check",1)

        if check not in [1,2]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数错误",
                             }, status=status.HTTP_200_OK)

        try:
            user = UserProfile.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该用户",
                             }, status=status.HTTP_200_OK)

        user.check = 1
        user.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """查看普通用户列表"""
        username = request.GET.get("username",None)
        phone = request.GET.get("phone",None)
        last_name = request.GET.get("last_name",None)
        order = request.GET.get("order",1)  # 1 按服务时长排序 2 按参加活动次数排序
        page = int(request.GET.get("page",1))
        pagesize = int(request.GET.get("pagesize",5))
        check = int(request.GET.get("check",0)) # 0 待审核 1 通过的 2未通过
        role = int(request.GET.get("role",0))   # 0,普通用户  2.教师

        if check not in [0,1,2] or role not in [0,1]:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "参数错误",
                         }, status=status.HTTP_200_OK)

        user = UserProfile.objects.filter(role=role,check=check)


        if username != None:
            user = user.filter(username=username)

        if phone != None:
            user = user.filter(phone=phone)

        if last_name != None:
            user = user.filter(last_name=last_name)

        serializer = UserDetailSerializer(instance=user.all(), many=True)


        if order == 1:
            data = sorted(serializer.data,key=operator.itemgetter("activity_time"),reverse=True)
        else:
            data = sorted(serializer.data, key=operator.itemgetter("activity_count"),reverse=True)

        data = data[(page - 1) * pagesize:(page - 1) * pagesize + pagesize]


        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"count": len(serializer.data), "data": data},
                         }, status=status.HTTP_200_OK)


class PasswordViewset(APIView):
    """修改密码接口"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, UserPermission)
    def put(self,request,*args,**kwargs):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserProfile.objects.get(id=request.user.id)
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

class OrganViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    """
       机构操作

    """
    serializer_class = OrganSerializer
    pagination_class = P1
    queryset = Organ.objects.filter().all()

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action == "create" or self.action == 'update' or self.action == 'destroy':
            return [IsAuthenticated(),AdminPermission()]
        elif self.action == "list" or self.action == "retrieve":
            return []

        return []


