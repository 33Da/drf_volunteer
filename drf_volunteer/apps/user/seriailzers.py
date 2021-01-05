# -*- coding: utf-8 -*-

# Date: 2019/8/5
# Name: serializers


from rest_framework import serializers,exceptions
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from apps.user.models import UserProfile,Organ
from apps.activity.models import UserandActivity
import datetime
import re


User = get_user_model()

def is_phone(phone):
    phone_pat = re.compile(r'^1[35678]\d{9}$')
    res = re.match(phone_pat, phone)

    if res != None:
        return True
    return False

def is_password(password):
    password_pat = re.compile("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$")
    res = re.match(password_pat,password)
    if res != None:
        return True
    return False

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=15, error_messages={"required": "不能为空"},
                                     style={'input_type': 'password'}, help_text="密码", label="密码")

    re_password = serializers.CharField(error_messages={"required": "不能为空"}, style={'input_type': 'password'},
                                        help_text="密码", label="密码")


    def validate(self, data):


        if not is_password(data["password"]):
            raise serializers.ValidationError("密码必须由数字和字母组成")

        if data["password"] != data["re_password"]:
            raise serializers.ValidationError("两次输入密码不一致")
        data.pop("re_password")

        return data



class RegisterSerializer(serializers.Serializer):
    """
    添加用户序列化类
    """
    id = serializers.CharField(read_only=True)

    username = serializers.CharField(max_length=10,min_length=10,error_messages={"required": "学号不能为空"}, validators=[UniqueValidator(queryset=User.objects.all(),message="学号存在了")])

    password = serializers.CharField(min_length=6, max_length=15, error_messages={"required": "不能为空"},
                                     style={'input_type': 'password'}, help_text="密码", label="密码")

    re_password = serializers.CharField(error_messages={"required": "不能为空"}, style={'input_type': 'password'},
                                        help_text="密码", label="密码")


    sex = serializers.IntegerField(error_messages={"required": "性别不能为空"},help_text="性别", label="性别")

    last_name = serializers.CharField(max_length=10,error_messages={"required": "姓名不能为空"},help_text="姓名", label="姓名")

    qq = serializers.CharField(max_length=30,required=False,help_text="qq", label="qq")

    weixin = serializers.CharField(max_length=100,required=False,help_text="weixin",label="weixin")

    email = serializers.EmailField(required=False,help_text="weixin",label="weixin")

    location = serializers.CharField(max_length=120,error_messages={"required": "地址不能为空"},help_text="地址",label="地址")

    myclass = serializers.IntegerField(error_messages={"required": "班级不能为空"},help_text="班级",label="班级")

    political = serializers.IntegerField(error_messages={"required": "政治面貌不能为空"},help_text="政治面貌",label="政治面貌")

    organ = serializers.IntegerField(error_messages={"required": "组织不能为空"},help_text="机构",label="机构")

    mail = serializers.CharField(max_length=30,required=False,help_text="邮政编码",label="邮政编码")

    phone = serializers.CharField(max_length=11,error_messages={"required": "电话不能为空"},help_text="手机号",label="手机号")

    def validate(self, data):

        if int(data["sex"]) not in [1,0]:
            raise serializers.ValidationError("性别错误")


        if data["political"] not in [0,1,2,3,4]:
            raise serializers.ValidationError("政治面貌信息错误")

        if not is_password(data["password"]):
            raise serializers.ValidationError("密码必须由数字和字母组成")

        if data["password"] != data["re_password"]:
            raise serializers.ValidationError("两次输入密码不一致")
        data.pop("re_password")

        if not is_phone(data["phone"]):
            raise serializers.ValidationError("手机格式错误")

        try:
            organ = Organ.objects.get(id=data["organ"])
            data["organ"] = organ
        except Exception as e:
            raise serializers.ValidationError("找不到该组织")

        return data


    def create(self, validated_data):
        user = UserProfile.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UpdateUserSerializer(serializers.Serializer):
    """
    修改用户序列化类
    """

    username = serializers.CharField(max_length=10, min_length=10, required=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="学号存在了")])



    sex = serializers.IntegerField(required=False, help_text="性别", label="性别")

    last_name = serializers.CharField(max_length=10,required=False, help_text="姓名", label="姓名")

    qq = serializers.CharField(max_length=30, required=False, help_text="qq", label="qq")

    weixin = serializers.CharField(max_length=100, required=False, help_text="weixin", label="weixin")

    email = serializers.EmailField(required=False, help_text="weixin", label="weixin")

    location = serializers.CharField(max_length=120, required=False, help_text="地址", label="地址")

    myclass = serializers.IntegerField(required=False, help_text="班级", label="班级")

    political = serializers.IntegerField(required=False, help_text="政治面貌", label="政治面貌")

    organ = serializers.IntegerField(required=False, help_text="机构", label="机构")

    mail = serializers.CharField(max_length=30, required=False, help_text="邮政编码", label="邮政编码")

    phone = serializers.CharField(max_length=11,required=False, help_text="手机号", label="手机号")

    def validate(self, data):

        if data.get("sex") is not None:
            if int(data["sex"]) not in [1, 0]:
                raise serializers.ValidationError("性别错误")

        if data.get("political") is not None:
            if data["political"] not in [0, 1, 2, 3, 4]:
                raise serializers.ValidationError("政治面貌信息错误")

        if data.get("phone") is not None:
            if not is_phone(data["phone"]):
                raise serializers.ValidationError("手机格式错误")

        if data.get("organ") is not None:
            try:
                organ = Organ.objects.get(id=data["organ"])
                data["organ"] = organ
            except Exception as e:
                raise serializers.ValidationError("手机格式错误")

        return data


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=15, error_messages={"required": "不能为空"},
                                     style={'input_type': 'password'}, help_text="密码", label="密码")

    re_password = serializers.CharField(error_messages={"required": "不能为空"}, style={'input_type': 'password'},
                                        help_text="密码", label="密码")

    def validate(self, data):

        if not is_password(data["password"]):
            raise serializers.ValidationError("密码必须由数字和字母组成")

        if data["password"] != data["re_password"]:
            raise serializers.ValidationError("两次输入密码不一致")
        data.pop("re_password")

        return data


class UserDetailSerializer(serializers.ModelSerializer):
    """用户信息"""
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    last_login = serializers.CharField(write_only=True)

    first_name = serializers.CharField(write_only=True)

    logintime = serializers.CharField(read_only=True)

    activity_count = serializers.SerializerMethodField(read_only=True)

    activity_time = serializers.SerializerMethodField(read_only=True)

    organ = serializers.CharField(source="organ.name")

    user_permissions = serializers.CharField( write_only=True)

    groups = serializers.CharField( write_only=True)

    is_active = serializers.CharField( write_only=True)

    is_staff = serializers.CharField( write_only=True)

    def get_activity_time(self,row):
        if row.role == 0: # 如果时普通用户
            myactivitys = UserandActivity.objects.filter(user=row).all() # 参加的活动数量

            myactivity_time = 0
            for myactivity in myactivitys:
                myactivity_time += myactivity.activity_time

            return myactivity_time
        else:
            return 0

    def get_activity_count(self, row):
        if row.role == 0:  # 如果时普通用户
            myactivitys = UserandActivity.objects.filter(user=row).count()  # 参加的活动数量

            return myactivitys
        else:
            return 0





    class Meta:
        model = UserProfile
        fields = "__all__"


class AdminSerializer(serializers.Serializer):
    """
    添加管理员序列化类
    """
    id = serializers.CharField(read_only=True)

    username = serializers.CharField(max_length=10, error_messages={"required": "账号不能为空"},
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="账号存在了")])

    password = serializers.CharField(min_length=6, max_length=15, error_messages={"required": "不能为空"},
                                     style={'input_type': 'password'}, help_text="密码", label="密码",write_only=True)

    re_password = serializers.CharField(error_messages={"required": "不能为空"}, style={'input_type': 'password'},
                                        help_text="密码", label="密码")

    last_name = serializers.CharField(max_length=10,error_messages={"required": "名称不能为空"},help_text="名称", label="名称")

    organ = serializers.IntegerField(error_messages={"required": "名称不能为空"})

    def validate(self, attrs):
        if not is_password(attrs["password"]):
            raise serializers.ValidationError("密码必须由数字和字母组成")

        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError("两次输入密码不一致")
        attrs.pop("re_password")

        try:
            organ = Organ.objects.get(id=attrs["organ"])
            attrs["organ"] = organ
        except Exception as e:
            raise serializers.ValidationError("找不到该组织")
        return attrs

    def create(self, validated_data):
        validated_data["role"] = 1
        validated_data["check"] = 1

        user = UserProfile.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class OrganSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Organ
        fields = "__all__"


class OrganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = "__all__"





