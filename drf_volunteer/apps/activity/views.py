from django.contrib.auth.backends import ModelBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from apps.activity.models import Ativity,UserandActivity,Type,Community,Communitypic,Histroy,HPic
from apps.user.models import Organ,UserProfile
from rest_framework import mixins
from rest_framework import viewsets
from .seriailzers import CreateActivityDetailSerializer,ActivityDetailSerializer,UpdataActivityDetailSerializer,UserandActivitySerializer,TypeSerializer,CommunitySerializer,CommunityUpdateSerializer,HistoryCreateSerializer,HistoryUpdateSerializer,HistorySerializer,AdminOrganSerializer
import datetime
import operator
from rest_framework import filters
from utils.permissions import UserPermission,AdminPermission,TeacherPermission
from utils.util import wite_to_excel
from django_filters.rest_framework import DjangoFilterBackend

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

# 管理员逻辑
class AdminAcivityViewset(APIView):
    """
    update:审核活动
    create:创建活动
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, AdminPermission)
    def put(self, request, *args, **kwargs):

        check = request.data.get("check",1)  # 0 不通过 其他 通过
        id =  request.data.get("id",0)
        content = request.data.get("content","活动不通过") # 拒绝理由默认：活动不通过

        try:
            ativity = Ativity.objects.get(id=id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到活动",
                             }, status=status.HTTP_200_OK)

        if ativity.status != 1:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该活动不需要审核",
                             }, status=status.HTTP_200_OK)

        if check == 0: # 不通过
            ativity.status = 10
            ativity.no_check = content
        else:
            ativity.status = 2

        ativity.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        """创建活动"""
        # 校验参数
        serializer = CreateActivityDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存
        validated_data = serializer.validated_data
        validated_data["people"] = request.user

        activity_pic = validated_data.pop("activity_pic")  # 另外处理这个

        activity = Ativity.objects.create(**validated_data)

        activity_pic.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S.png")
        activity.activity_pic =activity_pic
        activity.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def get(self,request,*args,**kwargs):
        activity = Ativity.objects.all()
        p1 = P1()
        page_list = p1.paginate_queryset(queryset=activity, request=request, view=self)

        serializer = CommunitySerializer(instance=page_list, many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"count": len(activity), "data": serializer.data},
                         }, status=status.HTTP_200_OK)


class AdminorganViewset(APIView):
    """组织数据分析"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, AdminPermission)
    def get(self,request,*args,**kwargs):

        organ = Organ.objects.all()
        order = int(request.GET.get("order",0))  # 0 activity_people_count 1 activity_count  2 activity_time_count
        page = int(request.GET.get("page", 1))
        pagesize = int(request.GET.get("pagesize", 5))
        reverse = int(request.GET.get("reverse", 0))  # False正序 True倒序

        if order not in [0, 1, 2] or reverse not in [0,1]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数错误",
                             }, status=status.HTTP_200_OK)


        serializer = AdminOrganSerializer(instance=organ,many=True)



        if order == 0:
            data = sorted(serializer.data, key=operator.itemgetter("activity_people_count"), reverse=reverse)
        elif order == 1:
            data = sorted(serializer.data, key=operator.itemgetter("activity_count"), reverse=reverse)
        else:
            data = sorted(serializer.data, key=operator.itemgetter("activity_time_count"), reverse=reverse)

        data = data[(page - 1) * pagesize:(page - 1) * pagesize + pagesize]

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"data":data,"count":len(serializer.data)},
                         }, status=status.HTTP_200_OK)



# 老师逻辑
class AcivityViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    """
    活动逻辑

    """
    serializer_class = ActivityDetailSerializer
    pagination_class = P1

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)

    # 过滤器
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('status',"type")
    ordering_fields  = ("createtime","hotcount")
    def get_queryset(self):
        return Ativity.objects.filter(people=self.request.user).all()

    def create(self, request, *args, **kwargs):
        """创建活动，这个接口仅普通管理员调"""
        # 校验参数
        serializer = CreateActivityDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存
        validated_data = serializer.validated_data
        validated_data["people"] = request.user

        activity_pic = validated_data.pop("activity_pic") # 另外处理这个

        activity = Ativity.objects.create(**validated_data)

        activity_pic.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S.png")

        activity.activity_pic = activity_pic
        activity.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """修改活动,这里留个bug，没做数据校验 ，超级管理员也是调用这个修改接口"""
        data = request.data


        # 校验参数
        serializer = UpdataActivityDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 修改
        validated_data = serializer.validated_data
        id = validated_data.pop("id")
        try:
            activity = Ativity.objects.get(id=id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到活动",
                             }, status=status.HTTP_200_OK)

        if activity.status != 0 and request.user.role == 1: # 普管
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该活动不能修改",
                             }, status=status.HTTP_200_OK)

        if activity.status != 2 and request.user.role == 2:  # 超管
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该活动不能修改",
                             }, status=status.HTTP_200_OK)

        if activity.people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该活动不能修改",
                             }, status=status.HTTP_200_OK)


        activity_pic = validated_data.pop("activity_pic",None)  # 另外处理这个


        Ativity.objects.filter(id=id).update(**validated_data)
        if activity_pic is not None:
            activity_pic.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S.png")
            activity.activity_pic = activity_pic
            activity.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)



class ActivityTimeViewset(APIView):
    """录入学生义工时以及评价"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)

    def put(self, request, *args, **kwargs):
        users = request.data.get("users","") # 这里是个列表里面是录入users id 1,2,3
        rank = request.data.get("rank",1) # 0 差 1 一般 2 优秀
        activity_time = int(request.data.get("activity_time",0)) # 义工时
        activity_id = request.data.get("id",0)

        try:
            activity = Ativity.objects.get(id=activity_id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "没有该活动",
                         }, status=status.HTTP_200_OK)

        if activity.status != 7:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该活动目前不能录入时长",
                             }, status=status.HTTP_200_OK)

        if rank not in [0,1,2]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "评价不准确",
                             }, status=status.HTTP_200_OK)

        if activity_time > activity.activity_time:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "义工时时长不得超过活动时长",
                             }, status=status.HTTP_200_OK)

        userslist = users.split(",")
        try:
            userandactivitys = UserandActivity.objects.filter(activity=activity,user__in=userslist).all()
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数格式不正确",
                             }, status=status.HTTP_200_OK)

        # 录入
        for userandactivity in userandactivitys:
            userandactivity.activity_time = activity_time
            userandactivity.rank = rank
            userandactivity.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "成功录入{0}个用户".format(len(userandactivitys)),
                         }, status=status.HTTP_200_OK)

class ActivityStatusViewset(APIView):
    """改变活动状态"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)

    def put(self, request, *args, **kwargs):
        activity_status = int(request.data.get("status")) # 要改变的状态
        id = request.data.get("id",0)

        try:
            ativity = Ativity.objects.get(id=id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到活动",
                             }, status=status.HTTP_200_OK)

        if ativity.people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该操作无效",
                             }, status=status.HTTP_200_OK)

        if activity_status not in [1,3,4,5,6,7,8,9]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该操作无效",
                             }, status=status.HTTP_200_OK)

        if activity_status == 1: # 提交审核
            if ativity.status != 0:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)

        if activity_status == 3:  # 发布活动
            if ativity.status != 2:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)

        if activity_status == 4:  # 开始报名
            if ativity.status != 3:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)

        if activity_status == 5:  # 结束报名
            if ativity.status != 4:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)

        if activity_status == 6:  # 活动中
            if ativity.status != 5:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)

        if activity_status == 7:  # 活动结束
            if ativity.status != 6:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)

        if activity_status == 9:  # 时长录入
            if ativity.status != 7:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)

        if activity_status == 8:  # 活动取消
            if ativity.status not in [3,4,5]:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "该操作无效",
                                 }, status=status.HTTP_200_OK)


        ativity.status = activity_status
        ativity.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

class AnalyseViewset(APIView):
    """主要时管理员首页"""

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)
    def get(self,request,*args,**kwargs):
        organ = request.user.organ

        users_queryset = UserProfile.objects.filter(organ=organ,role=0)

        # 注册人数
        regpeople = users_queryset.count()

        # 正式志愿者
        activitypeople = users_queryset.filter(check=1).count()

        # 男
        activityboy = users_queryset.filter(check=1,sex=0).count()

        # 女
        activitygirl = users_queryset.filter(check=1,sex=1).count()

        # 群众人数
        masses = users_queryset.filter(check=1,political=0).count()

        # 共青团员
        younger = users_queryset.filter(check=1,political=1).count()

        # 中共预备党员
        readymasses = users_queryset.filter(check=1, political=2).count()

        # 中共党员
        communistparty = users_queryset.filter(check=1, political=3).count()

        # 其它党派
        elseparty = users_queryset.filter(check=1, political=4).count()

        # 已完成活动
        endAtivity = Ativity.objects.filter(status=9).count()

        # 50个小时已上志愿者
        gooduser_count = 0
        for user in users_queryset.filter(check=1).all():
            useractivitys = UserandActivity.objects.filter(user=user,activity__status=9).all()
            time = 0
            for useractivity in useractivitys:
                time += useractivity.activity_time
            if time >= 50:
                gooduser_count += 1

        data = {
            "regpeople":regpeople,
            "activitypeople":activitypeople,
            "activityboy":activityboy,
            "activitygirl":activitygirl,
            "masses":masses,
            "younger":younger,
            "readymasses":readymasses,
            "communistparty":communistparty,
            "elseparty":elseparty,
            "endAtivity":endAtivity,
            "gooduser_count":gooduser_count
        }

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": data,
                         }, status=status.HTTP_200_OK)




class TypeViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


    serializer_class = TypeSerializer
    pagination_class = P1
    queryset = Type.objects.all()

    def get_permissions(self):
        if self.action == "create" or self.action == 'update' or self.action == 'destroy':
            return [IsAuthenticated(),AdminPermission()]
        elif self.action == "list" or self.action == "retrieve":
            return []


class CommunityViewset(viewsets.GenericViewSet):
    """社区"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)


    def create(self, request, *args, **kwargs):
        serializer = CommunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存
        validated_data = serializer.validated_data
        validated_data["publishuser"] = request.user

        community = Community.objects.create(**validated_data)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"id":community.id},
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = request.data.get("id",0)
        serializer = CommunityUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        try:
            community = Community.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该社区发言",
                             }, status=status.HTTP_200_OK)


        if community.publishuser != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有更改权限",
                             }, status=status.HTTP_200_OK)

        Community.objects.filter(id=id).update(**validated_data)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """社区列表,只能看到自己发布的"""

        communitys = Community.objects.filter(publishuser=request.user).all().order_by("updatetime")

        p1 = P1()
        page_list = p1.paginate_queryset(queryset=communitys, request=request, view=self)

        serializer = CommunitySerializer(instance=page_list, many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"count": len(communitys), "data": serializer.data},
                         }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk", 0)

        try:
            community = Community.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该社区发言",
                             }, status=status.HTTP_200_OK)

        if community.publishuser != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有更改权限",
                             }, status=status.HTTP_200_OK)

        community.delete()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk", 0)

        try:
            community = Community.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该社区发言",
                             }, status=status.HTTP_200_OK)

        if community.publishuser != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该社区发言",
                             }, status=status.HTTP_200_OK)

        serializer = CommunitySerializer(instance=community)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)


class CommunityPicViewset(APIView):
    """社区图片"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)

    def post(self,request,*args,**kwargs):
        pic = request.FILES.get("pic",None)
        id = request.data.get("id")

        if pic is None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "请上传图片",
                             }, status=status.HTTP_200_OK)

        try:
            community = Community.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该活动",
                             }, status=status.HTTP_200_OK)

        if community.publishuser != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有改社区修改权限",
                             }, status=status.HTTP_200_OK)

        pic.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S.png")
        Communitypic.objects.create(community=community,url=pic)


        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("pk", 0)

        try:
            communitypic = Communitypic.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该图片",
                             }, status=status.HTTP_200_OK)

        if communitypic.community.publishuser != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有更改权限",
                             }, status=status.HTTP_200_OK)

        communitypic.delete()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)



class HistroyViewset(viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)

    def create(self, request, *args, **kwargs):
        serializer = HistoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["activity"].people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你不能为该活动建立历史",
                             }, status=status.HTTP_200_OK)

        if serializer.validated_data["activity"].status not in [7,9]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你不能为该活动建立历史",
                             }, status=status.HTTP_200_OK)



        history = Histroy.objects.create(**serializer.validated_data)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"id": history.id},
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = request.data.get("id", 0)
        serializer = HistoryUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        try:
            history = Histroy.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该历史",
                             }, status=status.HTTP_200_OK)

        if history.activity.people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有更改权限",
                             }, status=status.HTTP_200_OK)

        Histroy.objects.filter(id=id).update(**validated_data)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """活动历史,只能看到自己发布的"""
        type_id = request.GET.get("type",0)

        try:
            type = Type.objects.get(id=type_id)
            history = Histroy.objects.filter(activity__people=request.user,activity__type=type).all().order_by("updatetime")
        except Exception as e:
            history = Histroy.objects.filter(activity__people=request.user).all().order_by("updatetime")


        p1 = P1()
        page_list = p1.paginate_queryset(queryset=history, request=request, view=self)

        serializer = HistorySerializer(instance=page_list, many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"count": len(history), "data": serializer.data},
                         }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk", 0)

        try:
            history = Histroy.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该历史",
                             }, status=status.HTTP_200_OK)

        if history.activity.people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有更改权限",
                             }, status=status.HTTP_200_OK)

        history.delete()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk", 0)

        try:
            history = Histroy.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该历史言",
                             }, status=status.HTTP_200_OK)

        if history.activity.people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该社区发言",
                             }, status=status.HTTP_200_OK)

        serializer = HistorySerializer(instance=history)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)

class HistroyPicViewset(viewsets.GenericViewSet):
    """社区图片"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,TeacherPermission)

    def create(self,request,*args,**kwargs):
        pic = request.FILES.get("pic",None)
        id = request.data.get("id")

        if pic is None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "请上传图片",
                             }, status=status.HTTP_200_OK)

        try:
            history = Histroy.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该历史活动",
                             }, status=status.HTTP_200_OK)

        if history.activity.people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有更改权限",
                             }, status=status.HTTP_200_OK)


        pic.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S.png")
        HPic.objects.create(history=history,url=pic)


        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk", 0)

        try:
            hpic = HPic.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该图片",
                             }, status=status.HTTP_200_OK)

        if hpic.histroy.activity.people != request.user:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有更改权限",
                             }, status=status.HTTP_200_OK)

        hpic.delete()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)






# 学生逻辑
class StuRegAcivityViewset(viewsets.GenericViewSet):
    """用户义工活动"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,UserPermission)
    def create(self,request,*args,**kwargs):

        id = request.data.get("id")

        try:
            activity = Ativity.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该活动",
                             }, status=status.HTTP_200_OK)

        if activity.status != 4:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该活动不能报名",
                             }, status=status.HTTP_200_OK)

        if request.user.role != 0 :
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "报名失败",
                             }, status=status.HTTP_200_OK)

        if UserandActivity.objects.filter(user=request.user,activity=activity).count() > 0:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "不能重复报名",
                             }, status=status.HTTP_200_OK)

        if UserandActivity.objects.filter(activity=activity).count() >= activity.people_count:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "已报满人数",
                             }, status=status.HTTP_200_OK)


        # 用户报名义工
        UserandActivity.objects.create(user=request.user,activity=activity)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self,request,*args,**kwargs):
        # 查看我报名的义工

        userandactivity = UserandActivity.objects.filter(user=request.user).all().order_by("signtime")

        p1 = P1()
        page_list = p1.paginate_queryset(queryset=userandactivity, request=request, view=self)

        serializer = UserandActivitySerializer(instance=page_list,many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"count":len(userandactivity),"data":serializer.data},
                         }, status=status.HTTP_200_OK)

    def retrieve(self,request,*args,**kwargs):
        # 查看一个报名的义工

        try:
            userandactivity = UserandActivity.objects.get(id=request.data.get("id"))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "未找到该比赛"
                             }, status=status.HTTP_200_OK)

        serializer = UserandActivitySerializer(instance=userandactivity)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [serializer.data],
                         }, status=status.HTTP_200_OK)

    def destroy(self,request,*args,**kwargs):
        """删除报名"""
        try:
            activity = Ativity.objects.get(id=kwargs.get("pk"))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "未找到该比赛"
                             }, status=status.HTTP_200_OK)

        if activity.status != 4:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "不能取消报名",
                             }, status=status.HTTP_200_OK)

        my_activity = UserandActivity.objects.filter(user=request.user,activity=activity).first()

        if my_activity is not None:
            my_activity.delete()
        else:
            Response({"status_code": status.HTTP_200_OK,
                      "message": "ok",
                      "results": "没有报名该比赛",
                      }, status=status.HTTP_200_OK)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class StuAcivityViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    """
     list：用户查看所有比赛
     retrieve：用户查看一个比赛信息
     create： 用户喜欢/取消喜欢比赛

    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,UserPermission)

    serializer_class = ActivityDetailSerializer
    pagination_class = P1
    queryset = Ativity.objects.filter(status__in=[3,4,5,6,7,8,9]).all()

    def create(self,request,*args,**kwargs):
        try:
            activity = Ativity.objects.get(id=request.data.get("id"))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该活动",
                             }, status=status.HTTP_200_OK)

        if request.user.role != 0:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你无法添加喜爱",
                             }, status=status.HTTP_200_OK)

        if activity.status not in [3,4,5,6,7,9]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你无法添加喜爱",
                             }, status=status.HTTP_200_OK)


        if request.user in activity.hot.all():  # 如果已经添加喜爱过了，就取消
            activity.hot.remove(request.user)
            activity.hotcount -= 1
            result = "删除成功"
        else: # 没喜爱过
            activity.hot.add(request.user)
            activity.hotcount += 1
            result = "添加成功"

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": result,
                         }, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        """查看活动"""
        statu = request.GET.get("status", 0)
        type_id = request.GET.get("type", 0)  # 0 看全部类型 看一个类型


        if int(statu) not in [3,4,5,6,7,8,9]: # 找能看的全部
            activity = Ativity.objects.filter(status__in=[3,4,5,6,7,8,9])
        else:
            activity = Ativity.objects.filter(status=statu)

        try:
            type = Type.objects.get(id=int(type_id))
            activity = activity.filter(type=type).order_by("activity_starttime")
        except Exception as e:
            activity = activity.order_by("activity_starttime")





        p1 = P1()
        page_list = p1.paginate_queryset(queryset=activity, request=request, view=self)

        serializer = ActivityDetailSerializer(instance=page_list, many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"count": len(activity), "data": serializer.data},
                         }, status=status.HTTP_200_OK)

class StuHistoryViewset(viewsets.GenericViewSet,mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,UserPermission)

    serializer_class = HistorySerializer
    pagination_class = P1
    queryset = Histroy.objects.filter(publishtime__lte=datetime.datetime.now()).all().order_by("publishtime")


class StuCommunityViewset(viewsets.GenericViewSet,mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,UserPermission)

    serializer_class = CommunitySerializer
    pagination_class = P1
    queryset = Community.objects.filter(publishtime__lte=datetime.datetime.now()).all().order_by("publishtime")

class GetPassStudentViewset(APIView):
    """获取通过综测的学生"""
    def get(self,request,*args,**kwargs):
        users = UserProfile.objects.filter(check=1,role=0).all()

        pass_list = []
        for user in users:
            useractivitys = UserandActivity.objects.filter(user=user, activity__status=9).all()
            time = 0
            for useractivity in useractivitys:
                time += useractivity.activity_time
            if time >= 10:  # 如果评测超过10
                pass_list.append((user.username,user.organ.name,user.myclass,time))

            # 表头
            excle_head = ["学号", "组织", "班别", "义工时"]

            # 写入数据到excel中
            ret = wite_to_excel("userlist", excle_head, pass_list)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": ret,
                         }, status=status.HTTP_200_OK)







