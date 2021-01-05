from rest_framework import serializers,exceptions

from rest_framework.validators import UniqueValidator
from apps.activity.models import Ativity,Organ,UserandActivity,Type,Community,Histroy
import datetime
from apps.user.seriailzers import OrganSerializer,UserDetailSerializer
from apps.user.models import UserProfile
import re

class AdminCreateActivitySerializer(serializers.Serializer):
    """超管创建活动序列化器"""
    organ = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="组织", label="组织")

    registration_time = serializers.DateField(error_messages={"required": "不能为空"},help_text="报名时间", label="报名时间")

    activity_time = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="活动时长", label="活动时长")

    link_phone = serializers.CharField(max_length=11,min_length=11,error_messages={"required": "不能为空"},help_text="联系电话", label="联系电话")

    activity_content = serializers.CharField(error_messages={"required": "不能为空"},help_text="义工内容", label="义工内容")

    link_pople = serializers.CharField(max_length=20,error_messages={"required": "不能为空"},help_text="联系人", label="联系人")

    people_count = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="人数", label="人数")

    title = serializers.CharField(error_messages={"required": "不能为空"},help_text="标题", label="标题")

    activity_starttime = serializers.DateTimeField(error_messages={"required": "不能为空"},help_text="活动时间", label="活动时间")

    type = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="活动类型", label="活动类型")

    status = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="保存方式", label="保存方式")
    def validate(self, data):
        if data["status"] not in [2,3]:
            raise serializers.ValidationError("status只能取待发布(2),已发布(3)两个状态")

        if data["registration_time"] < datetime.date.today():
            raise serializers.ValidationError("报名开始时间已过")

        if data["activity_starttime"].date() < data["registration_endtime"]:
            raise serializers.ValidationError("活动时间要大于报名结束时间")

        try:
            data["organ"] = Organ.objects.get(id=data["organ"])
        except Exception as e:
            raise serializers.ValidationError("找不到该组织")

        try:
            data["type"] = Type.objects.get(id=data["type"])
        except Exception as e:
            raise serializers.ValidationError("找不到该类型")

        return data

class CreateActivityDetailSerializer(serializers.Serializer):
    """创建活动序列化器"""
    organ = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="组织", label="组织")

    registration_time = serializers.DateField(error_messages={"required": "不能为空"},help_text="报名时间", label="报名时间")

    activity_time = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="活动时长", label="活动时长")

    link_phone = serializers.CharField(max_length=11,min_length=11,error_messages={"required": "不能为空"},help_text="联系电话", label="联系电话")

    activity_content = serializers.CharField(error_messages={"required": "不能为空"},help_text="义工内容", label="义工内容")

    link_pople = serializers.CharField(max_length=20,error_messages={"required": "不能为空"},help_text="联系人", label="联系人")

    people_count = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="人数", label="人数")

    title = serializers.CharField(error_messages={"required": "不能为空"},help_text="标题", label="标题")

    activity_starttime = serializers.DateTimeField(error_messages={"required": "不能为空"},help_text="活动时间", label="活动时间")

    type = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="活动类型", label="活动类型")

    activity_pic = serializers.FileField(error_messages={"required": "不能为空"})

    address = serializers.CharField(error_messages={"required": "不能为空"})
    def validate(self, data):
        if data["registration_time"] < datetime.date.today():
            raise serializers.ValidationError("活动时间已过")


        try:
            data["organ"] = Organ.objects.get(id=data["organ"])
        except Exception as e:
            raise serializers.ValidationError("找不到该组织")

        try:
            data["type"] = Type.objects.get(id=data["type"])
        except Exception as e:
            raise serializers.ValidationError("找不到该类型")

        return data

class ActivityDetailSerializer(serializers.ModelSerializer):
    """用户信息"""
    id = serializers.CharField(read_only=True)

    organ = OrganSerializer(many=False)

    type_name = serializers.CharField(source="type.name")


    user = serializers.SerializerMethodField() # 报名的人



    def get_user(self,row):
        users = []
        for u in row.user.all():
            users.append({"id":u.id,"name":u.username})

        return {"count":len(users),"sign_users":users}

    class Meta:
        model = Ativity
        fields = "__all__"

class UpdataActivityDetailSerializer(serializers.Serializer):
    """创建活动序列化器"""
    id = serializers.IntegerField(error_messages={"required": "不能为空"},help_text="活动id", label="活动id",required=False)

    organ = serializers.IntegerField(help_text="组织", label="组织",required=False)

    registration_time = serializers.DateField(help_text="报名时间", label="报名时间",required=False)

    activity_time = serializers.IntegerField(help_text="活动时长", label="活动时长",required=False)

    registration_endtime = serializers.DateField( help_text="报名结束时间", label="报名结束时间",required=False)

    link_phone = serializers.CharField(max_length=11,min_length=11,help_text="联系电话", label="联系电话",required=False)

    activity_content = serializers.CharField(help_text="义工内容", label="义工内容",required=False)

    link_pople = serializers.CharField(max_length=20,help_text="联系人", label="联系人",required=False)

    people_count = serializers.IntegerField(help_text="人数", label="人数",required=False)

    title = serializers.CharField(help_text="标题", label="标题",required=False)

    activity_starttime = serializers.DateTimeField(help_text="活动时间", label="活动时间",required=False)

    type = serializers.CharField(help_text="活动类型", label="活动类型",required=False)

    activity_pic = serializers.FileField(required=False)
    def validate(self, data):
        if data.get("organ") is not None:
            try:
                data["organ"] = Organ.objects.get(id=data["organ"])
            except Exception as e:
                raise serializers.ValidationError("找不到该组织")

        if data.get("type") is not None:
            try:
                data["type"] = Type.objects.get(id=data["type"])
            except Exception as e:
                raise serializers.ValidationError("找不到该类型")


        return data

class UserandActivitySerializer(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField()

    def get_activity(self,userandactivity):

        return {"id":userandactivity.activity.id,"title":userandactivity.activity.title}


    class Meta:
        model = UserandActivity
        fields = "__all__"

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

class CommunitySerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100,error_messages={"required": "不能为空"})

    publishtime = serializers.DateTimeField(error_messages={"required": "不能为空"})

    createtime = serializers.DateTimeField(read_only=True)

    updatetime = serializers.DateTimeField(read_only=True)

    pic = serializers.SerializerMethodField(read_only=True)


    def get_pic(self,row):
        pics = []
        for p in row.pic.all():
            pics.append({"id":p.id,"url":p.url.url})

        return {"count":len(pics),"data":pics}

    class Meta:
        model = Community
        fields = "__all__"

class CommunityUpdateSerializer(serializers.Serializer):


    title = serializers.CharField(max_length=100,required=False)

    publishtime = serializers.DateTimeField(required=False)


    content = serializers.CharField(required=False)

class HistoryCreateSerializer(serializers.Serializer):
    activity = serializers.IntegerField(error_messages={"required": "不能为空"})

    title = serializers.CharField(max_length=100,error_messages={"required": "不能为空"})

    content = serializers.CharField(error_messages={"required": "不能为空"})

    publishtime = serializers.DateTimeField(error_messages={"required": "不能为空"})

    def validate(self, attrs):
        try:
            attrs["activity"] = Ativity.objects.get(id=attrs["activity"])
        except Exception as e:
            raise serializers.ValidationError("没有该活动")

        return attrs

class HistoryUpdateSerializer(serializers.Serializer):


    title = serializers.CharField(max_length=100,required=False)

    publishtime = serializers.DateTimeField(required=False)


    content = serializers.CharField(required=False)

class HistorySerializer(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField(read_only=True)

    pic = serializers.SerializerMethodField(read_only=True)


    def get_pic(self,row):
        pics = []
        for p in row.pic.all():
            pics.append({"id":p.id,"url":p.url.url})

        return {"count":len(pics),"data":pics}

    def get_activity(self,row):
        return {"id":row.activity.id,"title":row.activity.title,"type":row.activity.type.name,"type_id":row.activity.type.id}



    class Meta:
        model = Histroy
        fields = "__all__"



class AdminOrganSerializer(serializers.ModelSerializer):
    # 用于管理员数据分析
    id = serializers.CharField(read_only=True)

    activity_count = serializers.SerializerMethodField(read_only=True)

    activity_people_count = serializers.SerializerMethodField(read_only=True)

    activity_time_count = serializers.SerializerMethodField(read_only=True)

    def get_activity_count(self,row):
        return row.activity.count()

    def get_activity_people_count(self, row):
        return UserProfile.objects.filter(organ=row,check=1,role=0).count()

    def get_activity_time_count(self, row):
        userandactivity = UserandActivity.objects.filter(activity__organ=row).all()
        time = 0
        for a in userandactivity:
            time += a.activity_time

        return time

    class Meta:
        model = Organ
        fields = "__all__"